/**
 * Kriptografi Hybrid - Main UI Utilities & Enhancements
 */

// Toast Notification Manager
function showToast(message, type = 'info', duration = 4000) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let iconSvg = '';
    if (type === 'success') {
        iconSvg = `<svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>`;
    } else if (type === 'error') {
        iconSvg = `<svg class="w-5 h-5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>`;
    } else {
        iconSvg = `<svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>`;
    }

    toast.innerHTML = `
        <div class="flex-shrink-0 mt-0.5">${iconSvg}</div>
        <div class="flex-1 text-sm font-medium leading-snug">${message}</div>
        <button type="button" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-lg leading-none" onclick="this.parentElement.remove()">&times;</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'toastFadeOut 0.3s forwards';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// Copy to Clipboard with Button Tooltip/State
async function copyText(text, btnElement, successMsg = 'Kunci berhasil disalin!') {
    if (!text || text.trim() === '') {
        showToast('Tidak ada teks untuk disalin!', 'error');
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        showToast(successMsg, 'success');

        if (btnElement) {
            const originalHtml = btnElement.innerHTML;
            btnElement.innerHTML = `
                <svg class="w-4 h-4 text-emerald-500 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg> Tersalin!
            `;
            setTimeout(() => {
                btnElement.innerHTML = originalHtml;
            }, 2000);
        }
    } catch (err) {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast(successMsg, 'success');
    }
}

// Download text content as a file (e.g. .pem or .txt)
function downloadTextFile(content, filename) {
    if (!content || content.trim() === '') {
        showToast('Konten kosong, tidak bisa diunduh!', 'error');
        return;
    }
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`File ${filename} berhasil diunduh!`, 'success');
}

// Format file sizes
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Setup custom drag & drop styling for file inputs
function setupDropZone(dropZoneId, inputId, previewContainerId) {
    const dropZone = document.getElementById(dropZoneId);
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(previewContainerId);

    if (!dropZone || !input) return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            input.files = e.dataTransfer.files;
            input.dispatchEvent(new Event('change'));
        }
    });

    dropZone.addEventListener('click', (e) => {
        if (e.target !== input) {
            input.click();
        }
    });

    input.addEventListener('change', () => {
        if (previewContainer && input.files && input.files[0]) {
            const file = input.files[0];
            previewContainer.innerHTML = `
                <div class="file-selected-badge animate-fade-in">
                    <svg class="w-5 h-5 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    <span class="font-semibold text-sm truncate max-w-xs">${file.name}</span>
                    <span class="text-xs bg-indigo-500 bg-opacity-10 text-indigo-500 dark:text-indigo-400 px-2 py-0.5 rounded-full font-mono">${formatFileSize(file.size)}</span>
                </div>
            `;
        }
    });
}
