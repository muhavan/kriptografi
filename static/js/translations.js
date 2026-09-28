/**
 * Kriptografi Hybrid - Bilingual Internationalization (i18n) Engine
 * Supports: Indonesian ('id') and English ('en')
 */

const translations = {
    id: {
        // Navbar & Brand
        brandName: "Kripto<span class=\"text-indigo-500\">Hybrid</span>",
        brandSub: "AES • RSA • ECC",
        engineActive: "Engine Aktif",
        navHome: "Beranda",
        navStudio: "Studio Enkripsi",
        navStartEncrypt: "Mulai Enkripsi",
        navMenu: "Menu Navigasi",
        toggleTheme: "Ganti Tema",

        // Footer
        footerTitle: "Kriptografi File Hybrid",
        footerDesc: "Keamanan berlapis tanpa kompromi dengan enkripsi simetris AES-256 dan tanda tangan digital ganda RSA & ECC.",
        footerDisclaimer: "Aplikasi Kriptografi File Hybrid — Dibuat untuk privasi dan integritas data tingkat militer.",
        zeroStorage: "Zero Permanent Storage • Client-Verified Security",
        copyright: "Dilisensikan © 17.6A.27",

        // Index / Home Page
        heroBadge: "Military-Grade Multi-Layer Cryptography",
        heroTitle1: "Keamanan Data Mutlak dengan",
        heroTitle2: "Enkripsi Hybrid Berlapis",
        heroDesc: "Kombinasi superior dari kecepatan enkripsi simetris <strong>AES-256</strong> serta kekuatan proteksi asimetris ganda <strong>RSA-2048</strong> dan <strong>ECC NIST-P256</strong>.",
        ctaStudio: "Buka Studio Enkripsi",
        ctaArchitecture: "Pelajari Cara Kerja",
        metricAes: "AES Simetris CBC",
        metricRsa: "RSA Asimetris OAEP",
        metricEcc: "Kurva Eliptik ECDSA",
        metricHash: "Hashing Integritas",

        // Pipeline Section
        pipelineTag: "Alur Pemrosesan Data",
        pipelineTitle: "Bagaimana Enkripsi Hybrid Bekerja?",
        pipelineSubtitle: "File Anda melalui 4 lapis pengamanan kriptografis secara otomatis sebelum disimpan atau dikirim.",
        step1Title: "1. Hashing Dokumen",
        step1Desc: "File diproses dengan fungsi <strong>SHA-256</strong> untuk menghasilkan sidik jari digital (hash) 256-bit unik yang mewakili integritas file asli.",
        step2Title: "2. Enkripsi AES-256",
        step2Desc: "Seluruh isi payload dokumen dienkripsi super cepat menggunakan kunci simetris <strong>AES-256 CBC</strong> acak yang dibuat dinamis saat itu juga.",
        step3Title: "3. Bungkus Kunci RSA",
        step3Desc: "Kunci AES rahasia dienkripsi dengan kunci publik <strong>RSA-2048 OAEP</strong>. Hanya pemilik kunci privat RSA yang bisa membuka kunci AES tersebut.",
        step4Title: "4. Tanda Tangan ECC",
        step4Desc: "File terenkripsi ditandatangani dengan kunci privat <strong>ECC (ECDSA)</strong> untuk menjamin autentikasi asal, non-repudiation, dan proteksi dari manipulasi.",

        // Comparison Section
        compTag: "Perbandingan Teknologi",
        compTitle: "Kekuatan Tiga Pilar Kriptografi",
        compDesc: "Setiap algoritma memiliki keunggulan khusus yang saling melengkapi dalam sistem hybrid ini.",
        compAesTitle: "AES (Advanced Encryption Standard)",
        compAesDesc: "Standar enkripsi data yang diadopsi pemerintah AS. Ideal untuk mengenkripsi file berukuran besar secara cepat tanpa membebani performa memori.",
        compAesSpeedLabel: "Kecepatan Enkripsi:",
        compAesSpeedVal: "Sangat Cepat (~Gbps)",
        compAesSizeLabel: "Ukuran Ciphertext:",
        compAesSizeVal: "Setara Plaintext",
        compAesRoleLabel: "Peran Sistem:",
        compAesRoleVal: "Enkripsi Payload File",

        compRsaTitle: "RSA (Rivest-Shamir-Adleman)",
        compRsaDesc: "Algoritma berbasis faktorisasi bilangan prima raksasa. Menghilangkan kebutuhan bertukar kunci simetris di saluran publik tanpa rasa takut disadap.",
        compRsaSecLabel: "Kekuatan Keamanan:",
        compRsaSecVal: "Standar Perbankan",
        compRsaProtLabel: "Proteksi Kunci:",
        compRsaProtVal: "Kunci Publik & Privat",
        compRsaRoleLabel: "Peran Sistem:",
        compRsaRoleVal: "Enkripsi Kunci AES",

        compEccTitle: "ECC (Elliptic Curve Cryptography)",
        compEccDesc: "Generasi modern kriptografi asimetris dengan panjang kunci lebih ringkas namun kekuatan matematis setara RSA 3072-bit.",
        compEccEffLabel: "Efisiensi Signature:",
        compEccEffVal: "Sangat Ringkas (64-byte)",
        compEccStrLabel: "Kekuatan Kunci:",
        compEccStrVal: "Ultra Tinggi",
        compEccRoleLabel: "Peran Sistem:",
        compEccRoleVal: "Tanda Tangan Integritas",

        ctaCardTag: "Mulai Sekarang",
        ctaCardTitle: "Amankan Berkas Rahasia Anda dalam Hitungan Detik",
        ctaCardDesc: "Hasilkan pasangan kunci RSA & ECC secara instan, upload dokumen apa pun (dokumen bisnis, kontrak hukum, sertifikat, atau gambar rahasia), dan download paket terenkripsi yang aman.",
        ctaCardBtn: "Mulai Enkripsi File",

        // Studio Page
        studioBadge: "Studio Keamanan Kriptografi",
        studioTitle: "Enkripsi, Verifikasi & Dekripsi File",
        studioDesc: "Sistem pengamanan data menyeluruh yang menggabungkan cipher simetris <strong>AES-256</strong> dengan autentikasi asimetris ganda <strong>RSA-2048</strong> dan <strong>ECC NIST-P256</strong>.",
        tabSign: "1. Enkripsi File",
        tabVerify: "2. Verifikasi Integritas",
        tabDecrypt: "3. Dekripsi Dokumen",

        // Tab 1: Sign
        keyGenTitle: "Generator Pasangan Kunci Kriptografi",
        keyGenDesc: "Buat pasangan kunci privat RSA-2048 & ECC NIST-P256 secara otomatis dan terstandar PEM.",
        btnGenKeys: "Generate Kunci Otomatis",
        btnGeneratingKeys: "Menghasilkan Kunci...",
        rsaKeyLabel: "Kunci Privat RSA (2048-bit)",
        eccKeyLabel: "Kunci Privat ECC (NIST-P256)",
        btnCopy: "Salin",
        btnDownload: "Unduh",
        rsaWarning: "Simpan kunci privat RSA ini baik-baik untuk proses dekripsi nanti.",
        eccNote: "Digunakan untuk menandatangani dokumen secara digital (Digital Signature).",
        placeholderRsa: "-----BEGIN PRIVATE KEY-----\nKlik tombol 'Generate Kunci Otomatis' di atas atau tempel kunci privat RSA Anda di sini...\n-----END PRIVATE KEY-----",
        placeholderEcc: "-----BEGIN EC PRIVATE KEY-----\nKlik tombol 'Generate Kunci Otomatis' di atas atau tempel kunci privat ECC Anda di sini...\n-----END EC PRIVATE KEY-----",

        step1BTitle: "Pilih Berkas untuk Dienkripsi",
        dropzonePrompt: "Tarik dan lepaskan file ke sini, atau",
        dropzoneChoose: "pilih dari perangkat",
        dropzoneFormats: "Format didukung: Dokumen (PDF, DOC, DOCX, TXT), Gambar (PNG, JPG, GIF), Kode & Data (JSON, MD, JS, HTML). Maksimal 16 MB.",
        btnSignAction: "Enkripsi & Tandatangani Berkas",
        btnSigningAction: "Mengenkripsi dengan AES-256 & ECC...",
        signSuccessTitle: "Berkas Berhasil Dienkripsi & Ditandatangani!",
        signSuccessDesc: "Payload file telah dilindungi dengan AES-256 dan kunci rahasianya dibungkus dengan RSA-2048 serta ditandatangani digital oleh ECC.",
        encryptedDocTitle: "Dokumen Terenkripsi (.bin)",
        encryptedDocDesc: "Berkas hasil enkripsi ciphertext AES-256 yang aman dibagikan.",
        btnDownloadEncrypted: "Download Dokumen Terenkripsi",
        metadataTitle: "File Metadata Kunci (.json)",
        metadataDesc: "Berisi kunci publik, hash SHA-256, dan tanda tangan digital untuk verifikasi.",
        btnDownloadMeta: "Download File Metadata",

        // Tab 2: Verify
        verifyStepTitle: "Verifikasi Keaslian & Integritas Dokumen",
        verifyStepDesc: "Unggah dokumen terenkripsi beserta file metadata miliknya. Sistem akan menguji integritas tanda tangan digital RSA dan ECC secara independen.",
        verifyLabel1: "1. Dokumen Terenkripsi",
        verifyLabel2: "2. File Metadata Kunci (.json)",
        dropzoneVerifyFilePrompt: "Pilih / Drag Dokumen Terenkripsi",
        dropzoneVerifyMetaPrompt: "Pilih / Drag File Metadata (.json)",
        btnVerifyAction: "Verifikasi Keaslian Dokumen",
        btnVerifyingAction: "Memverifikasi Tanda Tangan...",
        verifySuccessHeading: "DOKUMEN VALID & ASLI",
        verifySuccessSub: "Seluruh tanda tangan digital cocok. Berkas tidak pernah dimodifikasi atau dirusak sejak ditandatangani.",
        verifyFailHeading: "PERINGATAN: DOKUMEN TIDAK VALID / TELAH DIMODIFIKASI",
        verifyFailSub: "Verifikasi tanda tangan kriptografis gagal. Konten file tidak cocok dengan metadata aslinya.",
        origFilenamePrefix: "Nama Berkas Asli: ",
        sigTimePrefix: "Waktu Enkripsi: ",
        auditHash: "✓ Hash SHA-256 Match",
        auditRsa: "✓ RSA-PSS Signature Valid",
        auditEcc: "✓ ECC ECDSA Valid",

        // Tab 3: Decrypt
        decryptStepTitle: "Dekripsi Dokumen & Pratinjau Langsung",
        decryptStepDesc: "Untuk mendekripsi dokumen, masukkan file terenkripsi, file metadata miliknya, serta kunci privat RSA yang bersesuaian.",
        decryptLabel1: "1. Dokumen Terenkripsi",
        decryptLabel2: "2. File Metadata Kunci (.json)",
        rsaDecryptKeyLabel: "Kunci Privat RSA Pengirim / Pemilik",
        btnPaste: "Paste dari Clipboard",
        placeholderDecryptRsa: "Tempel kunci privat RSA (PEM format) yang digunakan saat enkripsi...",
        btnDecryptAction: "Dekripsi & Tampilkan Isi Dokumen",
        btnDecryptingAction: "Mendekripsi Dokumen...",
        decryptSuccessNotice: "Dokumen berhasil didekripsi dengan kunci AES rahasia!",
        previewHeading: "Pratinjau Isi Dokumen Asli:",
        btnDownloadDecrypted: "Download Dokumen Asli",
        noPreviewText: "Preview dokumen akan muncul di sini setelah didekripsi",

        // Toast Messages
        toastKeysGenerated: "Pasangan Kunci RSA-2048 & ECC berhasil dibuat!",
        toastKeysGenFail: "Gagal membuat kunci: ",
        toastSelectFile: "Silakan pilih berkas yang ingin dienkripsi terlebih dahulu!",
        toastKeysRequired: "Kedua kunci privat (RSA dan ECC) wajib diisi atau dibuat!",
        toastEncryptedSuccess: "Berkas berhasil dienkripsi dan ditandatangani!",
        toastNetworkError: "Terjadi kesalahan jaringan: ",
        toastSelectEncrypted: "Harap pilih dokumen terenkripsi terlebih dahulu!",
        toastSelectMeta: "Harap pilih file metadata kunci (.json)!",
        toastVerifyValid: "Dokumen ASLI dan Terverifikasi!",
        toastVerifyInvalid: "Dokumen TIDAK VALID atau telah diubah!",
        toastVerifyError: "Kesalahan verifikasi: ",
        toastSelectDecryptFile: "Pilih dokumen terenkripsi yang ingin didekripsi!",
        toastRsaRequired: "Kunci privat RSA diperlukan untuk membuka kunci AES!",
        toastDecryptedSuccess: "Dokumen berhasil didekripsi!",
        toastDecryptedFail: "Gagal mendekripsi: ",
        toastCopied: " disalin ke clipboard!",
        toastPasted: "Kunci berhasil ditempel dari clipboard!",
        toastEmptyCopy: "Tidak ada teks untuk disalin!",
        toastDownloaded: " berhasil diunduh!"
    },

    en: {
        // Navbar & Brand
        brandName: "Crypto<span class=\"text-indigo-500\">Hybrid</span>",
        brandSub: "AES • RSA • ECC",
        engineActive: "Engine Active",
        navHome: "Home",
        navStudio: "Encryption Studio",
        navStartEncrypt: "Start Encrypt",
        navMenu: "Navigation Menu",
        toggleTheme: "Toggle Theme",

        // Footer
        footerTitle: "Hybrid File Cryptography",
        footerDesc: "Uncompromising multi-layer security combining AES-256 symmetric cipher with dual RSA & ECC digital signatures.",
        footerDisclaimer: "Hybrid File Cryptography Suite — Engineered for military-grade privacy and data integrity.",
        zeroStorage: "Zero Permanent Storage • Client-Verified Security",
        copyright: "Licensed © 17.6A.27",

        // Index / Home Page
        heroBadge: "Military-Grade Multi-Layer Cryptography",
        heroTitle1: "Absolute Data Security with",
        heroTitle2: "Multi-Layer Hybrid Encryption",
        heroDesc: "Superior synergy of <strong>AES-256</strong> high-speed symmetric encryption with dual asymmetric protection of <strong>RSA-2048</strong> and <strong>ECC NIST-P256</strong>.",
        ctaStudio: "Open Encryption Studio",
        ctaArchitecture: "Explore Architecture",
        metricAes: "AES Symmetric CBC",
        metricRsa: "RSA Asymmetric OAEP",
        metricEcc: "Elliptic Curve ECDSA",
        metricHash: "Integrity Hashing",

        // Pipeline Section
        pipelineTag: "Data Processing Pipeline",
        pipelineTitle: "How Does Hybrid Encryption Work?",
        pipelineSubtitle: "Your files automatically pass through 4 cryptographic protection layers before storage or transfer.",
        step1Title: "1. Document Hashing",
        step1Desc: "The file is processed with <strong>SHA-256</strong> to generate a unique 256-bit digital fingerprint (hash) representing original integrity.",
        step2Title: "2. AES-256 Encryption",
        step2Desc: "The entire document payload is encrypted at maximum speed using a dynamic, randomly generated <strong>AES-256 CBC</strong> symmetric key.",
        step3Title: "3. RSA Key Wrapping",
        step3Desc: "The secret AES key is wrapped with the recipient's <strong>RSA-2048 OAEP</strong> public key. Only the RSA private key can unlock it.",
        step4Title: "4. ECC Digital Signature",
        step4Desc: "The encrypted file is digitally signed with an <strong>ECC (ECDSA)</strong> private key to guarantee origin authenticity and non-repudiation.",

        // Comparison Section
        compTag: "Technology Breakdown",
        compTitle: "Power of Three Cryptographic Pillars",
        compDesc: "Each cipher delivers specialized strengths that complement each other seamlessly in this hybrid system.",
        compAesTitle: "AES (Advanced Encryption Standard)",
        compAesDesc: "Adopted as the worldwide symmetric encryption benchmark. Ideal for high-speed file encryption without memory exhaustion.",
        compAesSpeedLabel: "Encryption Speed:",
        compAesSpeedVal: "Blazing Fast (~Gbps)",
        compAesSizeLabel: "Ciphertext Size:",
        compAesSizeVal: "Equal to Plaintext",
        compAesRoleLabel: "System Role:",
        compAesRoleVal: "File Payload Encryption",

        compRsaTitle: "RSA (Rivest-Shamir-Adleman)",
        compRsaDesc: "Built upon the mathematical hardness of giant prime factorization. Eliminates symmetric key exchange risks over public networks.",
        compRsaSecLabel: "Security Rating:",
        compRsaSecVal: "Banking Standard",
        compRsaProtLabel: "Key Protection:",
        compRsaProtVal: "Public & Private Key Pair",
        compRsaRoleLabel: "System Role:",
        compRsaRoleVal: "AES Key Wrapping",

        compEccTitle: "ECC (Elliptic Curve Cryptography)",
        compEccDesc: "Modern asymmetric cryptography delivering ultra-compact keys with mathematical resistance equivalent to RSA 3072-bit.",
        compEccEffLabel: "Signature Efficiency:",
        compEccEffVal: "Ultra Compact (64-byte)",
        compEccStrLabel: "Key Hardness:",
        compEccStrVal: "Ultra High",
        compEccRoleLabel: "System Role:",
        compEccRoleVal: "Integrity Digital Signature",

        ctaCardTag: "Get Started Now",
        ctaCardTitle: "Protect Your Sensitive Documents in Seconds",
        ctaCardDesc: "Instantly generate RSA & ECC keypairs, upload any file (business contracts, legal agreements, certificates, or private photos), and download your encrypted archive.",
        ctaCardBtn: "Start File Encryption",

        // Studio Page
        studioBadge: "Cryptography Security Studio",
        studioTitle: "Encrypt, Verify & Decrypt Files",
        studioDesc: "Complete data protection system combining <strong>AES-256</strong> symmetric cipher with dual asymmetric authentication of <strong>RSA-2048</strong> and <strong>ECC NIST-P256</strong>.",
        tabSign: "1. Encrypt File",
        tabVerify: "2. Verify Integrity",
        tabDecrypt: "3. Decrypt Document",

        // Tab 1: Sign
        keyGenTitle: "Cryptographic Keypair Generator",
        keyGenDesc: "Generate standard PEM-encoded RSA-2048 & ECC NIST-P256 private keys automatically.",
        btnGenKeys: "Auto-Generate Keys",
        btnGeneratingKeys: "Generating Keys...",
        rsaKeyLabel: "RSA Private Key (2048-bit)",
        eccKeyLabel: "ECC Private Key (NIST-P256)",
        btnCopy: "Copy",
        btnDownload: "Download",
        rsaWarning: "Keep this RSA private key safe; it is strictly required to decrypt your document later.",
        eccNote: "Used to sign the document payload digitally (Digital Signature).",
        placeholderRsa: "-----BEGIN PRIVATE KEY-----\nClick 'Auto-Generate Keys' above or paste your RSA private key here...\n-----END PRIVATE KEY-----",
        placeholderEcc: "-----BEGIN EC PRIVATE KEY-----\nClick 'Auto-Generate Keys' above or paste your ECC private key here...\n-----END EC PRIVATE KEY-----",

        step1BTitle: "Select File to Encrypt",
        dropzonePrompt: "Drag and drop file here, or",
        dropzoneChoose: "browse from device",
        dropzoneFormats: "Supported formats: Documents (PDF, DOC, DOCX, TXT), Images (PNG, JPG, GIF), Code & Data (JSON, MD, JS, HTML). Max 16 MB.",
        btnSignAction: "Encrypt & Sign File",
        btnSigningAction: "Encrypting with AES-256 & ECC...",
        signSuccessTitle: "File Encrypted & Signed Successfully!",
        signSuccessDesc: "The file payload is encrypted with AES-256, its secret key wrapped with RSA-2048, and signed digitally by ECC.",
        encryptedDocTitle: "Encrypted Document (.bin)",
        encryptedDocDesc: "AES-256 ciphertext payload file that is safe to share publicly.",
        btnDownloadEncrypted: "Download Encrypted File",
        metadataTitle: "Key Metadata File (.json)",
        metadataDesc: "Contains public keys, SHA-256 hash, and digital signatures for integrity verification.",
        btnDownloadMeta: "Download Metadata File",

        // Tab 2: Verify
        verifyStepTitle: "Verify Document Authenticity & Integrity",
        verifyStepDesc: "Upload the encrypted document alongside its key metadata file. The system independently verifies both RSA and ECC digital signatures.",
        verifyLabel1: "1. Encrypted Document",
        verifyLabel2: "2. Key Metadata File (.json)",
        dropzoneVerifyFilePrompt: "Select / Drag Encrypted Document",
        dropzoneVerifyMetaPrompt: "Select / Drag Metadata File (.json)",
        btnVerifyAction: "Verify Document Authenticity",
        btnVerifyingAction: "Verifying Signatures...",
        verifySuccessHeading: "DOCUMENT VALID & AUTHENTIC",
        verifySuccessSub: "All cryptographic digital signatures match. Document has never been altered since signing.",
        verifyFailHeading: "WARNING: DOCUMENT INVALID / TAMPERED WITH",
        verifyFailSub: "Cryptographic signature verification failed. Document content does not match original metadata.",
        origFilenamePrefix: "Original Filename: ",
        sigTimePrefix: "Encryption Time: ",
        auditHash: "✓ SHA-256 Hash Match",
        auditRsa: "✓ RSA-PSS Signature Valid",
        auditEcc: "✓ ECC ECDSA Valid",

        // Tab 3: Decrypt
        decryptStepTitle: "Decrypt Document & Live Preview",
        decryptStepDesc: "To decrypt the document, provide the encrypted file, its metadata file, and the corresponding RSA private key.",
        decryptLabel1: "1. Encrypted Document",
        decryptLabel2: "2. Key Metadata File (.json)",
        rsaDecryptKeyLabel: "Sender / Owner's RSA Private Key",
        btnPaste: "Paste from Clipboard",
        placeholderDecryptRsa: "Paste the RSA private key (PEM format) used during encryption...",
        btnDecryptAction: "Decrypt & Preview Content",
        btnDecryptingAction: "Decrypting Document...",
        decryptSuccessNotice: "Document decrypted successfully using the recovered AES secret key!",
        previewHeading: "Original Document Preview:",
        btnDownloadDecrypted: "Download Original Document",
        noPreviewText: "Document preview will appear here once decrypted",

        // Toast Messages
        toastKeysGenerated: "RSA-2048 & ECC Keypair generated successfully!",
        toastKeysGenFail: "Failed to generate keys: ",
        toastSelectFile: "Please select a file to encrypt first!",
        toastKeysRequired: "Both RSA and ECC private keys are required!",
        toastEncryptedSuccess: "File encrypted and digitally signed successfully!",
        toastNetworkError: "Network error occurred: ",
        toastSelectEncrypted: "Please select the encrypted file first!",
        toastSelectMeta: "Please select the key metadata file (.json)!",
        toastVerifyValid: "Document is AUTHENTIC and Verified!",
        toastVerifyInvalid: "Document is INVALID or has been tampered with!",
        toastVerifyError: "Verification error: ",
        toastSelectDecryptFile: "Please select the encrypted file to decrypt!",
        toastRsaRequired: "RSA private key is required to decrypt the AES key!",
        toastDecryptedSuccess: "Document decrypted successfully!",
        toastDecryptedFail: "Failed to decrypt: ",
        toastCopied: " copied to clipboard!",
        toastPasted: "Key pasted successfully from clipboard!",
        toastEmptyCopy: "No text to copy!",
        toastDownloaded: " downloaded successfully!"
    }
};

// Current active language: default 'id', fallback to 'en'
let currentLang = localStorage.getItem('language') || 'id';

// Translation lookup helper
function t(key) {
    if (translations[currentLang] && translations[currentLang][key]) {
        return translations[currentLang][key];
    }
    if (translations['en'] && translations['en'][key]) {
        return translations['en'][key];
    }
    return key;
}

// Apply language across all DOM elements with data-i18n attributes
function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    localStorage.setItem('language', lang);
    document.documentElement.lang = lang;

    // Update innerHTML of elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang][key]) {
            el.placeholder = translations[lang][key];
        }
    });

    // Update titles
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (translations[lang][key]) {
            el.title = translations[lang][key];
        }
    });

    // Update language switcher buttons active states
    document.querySelectorAll('.lang-btn').forEach(btn => {
        const btnLang = btn.getAttribute('data-lang');
        if (btnLang === lang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Trigger an event so custom components can refresh if needed
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
}

// Auto-initialize language on page load
document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLang);

    // Setup click handlers for all language buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const chosenLang = btn.getAttribute('data-lang');
            if (chosenLang) {
                setLanguage(chosenLang);
            }
        });
    });
});
