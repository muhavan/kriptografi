/**
 * Kriptografi Hybrid - Client-Side Native Web Cryptography Engine
 * Algorithms:
 *  - AES-256 (CBC mode with PKCS#7 padding) for symmetric payload encryption
 *  - RSA-2048 (OAEP SHA-256 for key wrapping, PSS SHA-256 for integrity signature)
 *  - ECC NIST-P256 (ECDSA SHA-256 for payload digital signature)
 *  - SHA-256 for document hashing
 * 
 * Runs 100% in-browser via window.crypto.subtle (Zero-Knowledge & Zero Server Dependency).
 */

const CryptoEngine = (() => {
    const subtle = window.crypto.subtle;

    // --- Format Converters & Helpers ---
    function arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return btoa(binary);
    }

    function base64ToArrayBuffer(base64) {
        const binary = atob(base64.trim());
        const len = binary.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binary.charCodeAt(i);
        }
        return bytes.buffer;
    }

    function arrayBufferToHex(buffer) {
        return Array.from(new Uint8Array(buffer))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    function derToPem(buffer, header) {
        const b64 = arrayBufferToBase64(buffer);
        const formatted = b64.match(/.{1,64}/g).join('\n');
        return `-----BEGIN ${header}-----\n${formatted}\n-----END ${header}-----`;
    }

    function pemToDer(pem) {
        const clean = pem
            .replace(/-----BEGIN [^-]+-----/g, '')
            .replace(/-----END [^-]+-----/g, '')
            .replace(/\s+/g, '');
        return base64ToArrayBuffer(clean);
    }

    // --- 1. Key Generation ---

    /**
     * Generate RSA-2048 Key Pair (PKCS#8 PEM)
     */
    async function generateRsaKeys() {
        const keyPair = await subtle.generateKey(
            {
                name: "RSA-OAEP",
                modulusLength: 2048,
                publicExponent: new Uint8Array([1, 0, 1]),
                hash: "SHA-256"
            },
            true,
            ["encrypt", "decrypt"]
        );

        const privDer = await subtle.exportKey("pkcs8", keyPair.privateKey);
        const pubDer = await subtle.exportKey("spki", keyPair.publicKey);

        return {
            privateKey: derToPem(privDer, "PRIVATE KEY"),
            publicKey: derToPem(pubDer, "PUBLIC KEY")
        };
    }

    /**
     * Generate ECC NIST-P256 Key Pair (PKCS#8 PEM)
     */
    async function generateEccKeys() {
        const keyPair = await subtle.generateKey(
            {
                name: "ECDSA",
                namedCurve: "P-256"
            },
            true,
            ["sign", "verify"]
        );

        const privDer = await subtle.exportKey("pkcs8", keyPair.privateKey);
        const pubDer = await subtle.exportKey("spki", keyPair.publicKey);

        return {
            privateKey: derToPem(privDer, "PRIVATE KEY"),
            publicKey: derToPem(pubDer, "PUBLIC KEY")
        };
    }

    // --- Helper: Extract Public Key from Private Key PEM via JWK ---
    async function deriveRsaPublicKey(privateKeyPem) {
        const privDer = pemToDer(privateKeyPem);
        const privKey = await subtle.importKey(
            "pkcs8",
            privDer,
            { name: "RSA-OAEP", hash: "SHA-256" },
            true,
            ["decrypt"]
        );
        const jwk = await subtle.exportKey("jwk", privKey);
        const pubJwk = {
            kty: jwk.kty,
            n: jwk.n,
            e: jwk.e,
            alg: "RSA-OAEP-256",
            ext: true
        };
        const pubKey = await subtle.importKey(
            "jwk",
            pubJwk,
            { name: "RSA-OAEP", hash: "SHA-256" },
            true,
            ["encrypt"]
        );
        const spkiDer = await subtle.exportKey("spki", pubKey);
        return {
            keyObj: pubKey,
            pem: derToPem(spkiDer, "PUBLIC KEY")
        };
    }

    async function deriveEccPublicKey(privateKeyPem) {
        const privDer = pemToDer(privateKeyPem);
        const privKey = await subtle.importKey(
            "pkcs8",
            privDer,
            { name: "ECDSA", namedCurve: "P-256" },
            true,
            ["sign"]
        );
        const jwk = await subtle.exportKey("jwk", privKey);
        const pubJwk = {
            kty: "EC",
            crv: jwk.crv,
            x: jwk.x,
            y: jwk.y,
            ext: true
        };
        const pubKey = await subtle.importKey(
            "jwk",
            pubJwk,
            { name: "ECDSA", namedCurve: "P-256" },
            true,
            ["verify"]
        );
        const spkiDer = await subtle.exportKey("spki", pubKey);
        return {
            keyObj: pubKey,
            pem: derToPem(spkiDer, "PUBLIC KEY")
        };
    }

    // --- 2. Sign & Encrypt Document (Hybrid Process) ---
    async function signAndEncryptDocument(file, rsaPrivateKeyPem, eccPrivateKeyPem) {
        const fileBuffer = await file.arrayBuffer();

        // 1. Calculate document SHA-256 hash
        const hashBuffer = await subtle.digest("SHA-256", fileBuffer);
        const docHash = arrayBufferToHex(hashBuffer);

        // 2. Sign document hash with RSA-PSS
        const rsaPrivDer = pemToDer(rsaPrivateKeyPem);
        const rsaPssPrivKey = await subtle.importKey(
            "pkcs8",
            rsaPrivDer,
            { name: "RSA-PSS", hash: "SHA-256" },
            false,
            ["sign"]
        );
        const rsaSigBuffer = await subtle.sign(
            { name: "RSA-PSS", saltLength: 32 },
            rsaPssPrivKey,
            new TextEncoder().encode(docHash)
        );
        const rsaSignatureB64 = arrayBufferToBase64(rsaSigBuffer);

        // 3. Encrypt document with dynamic AES-256-CBC
        const aesKey = await subtle.generateKey(
            { name: "AES-CBC", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );
        const rawAesKey = await subtle.exportKey("raw", aesKey);
        const iv = window.crypto.getRandomValues(new Uint8Array(16));
        const ciphertextBuffer = await subtle.encrypt(
            { name: "AES-CBC", iv: iv },
            aesKey,
            fileBuffer
        );

        // Concatenate IV + Ciphertext
        const encryptedData = new Uint8Array(iv.byteLength + ciphertextBuffer.byteLength);
        encryptedData.set(iv, 0);
        encryptedData.set(new Uint8Array(ciphertextBuffer), iv.byteLength);

        // 4. Wrap AES key with RSA-OAEP
        const rsaPub = await deriveRsaPublicKey(rsaPrivateKeyPem);
        const encryptedAesKeyBuffer = await subtle.encrypt(
            { name: "RSA-OAEP" },
            rsaPub.keyObj,
            rawAesKey
        );
        const encryptedAesKeyB64 = arrayBufferToBase64(encryptedAesKeyBuffer);

        // 5. Sign encrypted binary payload with ECC-ECDSA
        const eccPrivDer = pemToDer(eccPrivateKeyPem);
        const eccPrivKey = await subtle.importKey(
            "pkcs8",
            eccPrivDer,
            { name: "ECDSA", namedCurve: "P-256" },
            false,
            ["sign"]
        );
        const eccSigBuffer = await subtle.sign(
            { name: "ECDSA", hash: { name: "SHA-256" } },
            eccPrivKey,
            encryptedData
        );
        const eccSignatureB64 = arrayBufferToBase64(eccSigBuffer);
        const eccPub = await deriveEccPublicKey(eccPrivateKeyPem);

        // 6. Build Metadata JSON
        const metadata = {
            rsa_public_key: rsaPub.pem,
            ecc_public_key: eccPub.pem,
            filename: file.name,
            timestamp: new Date().toISOString(),
            doc_hash: docHash,
            rsa_signature: rsaSignatureB64,
            ecc_signature: eccSignatureB64,
            encrypted_aes_key: encryptedAesKeyB64
        };

        const encryptedBlob = new Blob([encryptedData], { type: "application/octet-stream" });
        const metadataBlob = new Blob([JSON.stringify(metadata, null, 2)], { type: "application/json" });

        return {
            encryptedBlob,
            metadataBlob,
            metadata,
            encryptedFilename: `encrypted_${file.name}.bin`,
            metadataFilename: `metadata_${file.name}.json`
        };
    }

    // --- 3. Verify Document Integrity ---
    async function verifyDocument(encryptedFileBuffer, metadata) {
        try {
            if (!metadata.rsa_public_key || !metadata.ecc_public_key) {
                return { valid: false, error: "Public keys not found in metadata JSON" };
            }

            const encryptedBytes = new Uint8Array(encryptedFileBuffer);

            // 1. Verify ECC signature on encrypted file payload
            const eccPubDer = pemToDer(metadata.ecc_public_key);
            const eccPubKey = await subtle.importKey(
                "spki",
                eccPubDer,
                { name: "ECDSA", namedCurve: "P-256" },
                false,
                ["verify"]
            );
            const eccSigBytes = base64ToArrayBuffer(metadata.ecc_signature);
            const eccValid = await subtle.verify(
                { name: "ECDSA", hash: { name: "SHA-256" } },
                eccPubKey,
                eccSigBytes,
                encryptedBytes
            );

            if (!eccValid) {
                return {
                    valid: false,
                    error: "ECC signature verification failed. Document may have been modified or corrupted."
                };
            }

            // 2. Verify RSA signature on document hash
            const rsaPubDer = pemToDer(metadata.rsa_public_key);
            const rsaPubKey = await subtle.importKey(
                "spki",
                rsaPubDer,
                { name: "RSA-PSS", hash: "SHA-256" },
                false,
                ["verify"]
            );
            const rsaSigBytes = base64ToArrayBuffer(metadata.rsa_signature);
            const rsaValid = await subtle.verify(
                { name: "RSA-PSS", saltLength: 32 },
                rsaPubKey,
                rsaSigBytes,
                new TextEncoder().encode(metadata.doc_hash)
            );

            if (!rsaValid) {
                return {
                    valid: false,
                    error: "RSA signature verification failed. Document hash signature does not match."
                };
            }

            return {
                valid: true,
                filename: metadata.filename,
                timestamp: metadata.timestamp,
                doc_hash: metadata.doc_hash,
                metadata: metadata
            };
        } catch (err) {
            return {
                valid: false,
                error: `Verification error: ${err.message}`
            };
        }
    }

    // --- 4. Decrypt Document ---
    async function decryptDocument(encryptedFileBuffer, metadata, rsaPrivateKeyPem) {
        try {
            // First verify document signatures
            const verifyRes = await verifyDocument(encryptedFileBuffer, metadata);
            if (!verifyRes.valid) {
                return {
                    success: false,
                    error: `Verification failed before decryption: ${verifyRes.error}`
                };
            }

            // Decrypt AES key with RSA-OAEP
            const rsaPrivDer = pemToDer(rsaPrivateKeyPem);
            let rsaPrivKey;
            try {
                rsaPrivKey = await subtle.importKey(
                    "pkcs8",
                    rsaPrivDer,
                    { name: "RSA-OAEP", hash: "SHA-256" },
                    false,
                    ["decrypt"]
                );
            } catch (err) {
                return {
                    success: false,
                    error: "Invalid RSA Private Key format. Please ensure valid PKCS#8 PEM."
                };
            }

            const encAesKeyBytes = base64ToArrayBuffer(metadata.encrypted_aes_key);
            let rawAesKey;
            try {
                rawAesKey = await subtle.decrypt(
                    { name: "RSA-OAEP" },
                    rsaPrivKey,
                    encAesKeyBytes
                );
            } catch (err) {
                return {
                    success: false,
                    error: "Failed to decrypt AES key. Please verify that you provided the matching RSA private key."
                };
            }

            // Decrypt file payload with AES-CBC
            const aesKey = await subtle.importKey(
                "raw",
                rawAesKey,
                { name: "AES-CBC" },
                false,
                ["decrypt"]
            );

            const encryptedBytes = new Uint8Array(encryptedFileBuffer);
            const iv = encryptedBytes.slice(0, 16);
            const ciphertext = encryptedBytes.slice(16);

            let decryptedBuffer;
            try {
                decryptedBuffer = await subtle.decrypt(
                    { name: "AES-CBC", iv: iv },
                    aesKey,
                    ciphertext
                );
            } catch (err) {
                return {
                    success: false,
                    error: "Failed to decrypt payload with AES key. Ciphertext may be corrupt."
                };
            }

            // Verify decrypted data hash matches original doc_hash
            const decHashBuffer = await subtle.digest("SHA-256", decryptedBuffer);
            const decHash = arrayBufferToHex(decHashBuffer);
            if (decHash !== metadata.doc_hash) {
                return {
                    success: false,
                    error: "Decrypted document hash mismatch! The content has been compromised."
                };
            }

            const filename = metadata.filename || "decrypted_file";
            const decryptedBlob = new Blob([decryptedBuffer]);

            return {
                success: true,
                filename: filename,
                blob: decryptedBlob,
                buffer: decryptedBuffer
            };
        } catch (err) {
            return {
                success: false,
                error: `Decryption error: ${err.message}`
            };
        }
    }

    return {
        generateRsaKeys,
        generateEccKeys,
        signAndEncryptDocument,
        verifyDocument,
        decryptDocument
    };
})();
