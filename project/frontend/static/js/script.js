/**
 * Check if the user has selected an image to upload. If not, prevent the form from submitting.
 */
document.getElementById('form').addEventListener('submit', function(event) {
    let input = document.getElementById('input-file');
    let src_language = document.getElementById('src-language').value;
    let tgt_language = document.getElementById('tgt-language').value;

    if (input.files.length === 0) {
        event.preventDefault();
        alert('Please select an image to upload.');
    }
    else if (src_language === tgt_language) {
        event.preventDefault();
        alert('Please select different languages for source and target language.');
    }
});


/**
 * Read image file and display it in the preview. Change the label to the file name.
 * @param {*} input
 */
function onImageSelection(input) {
    const file = input.files[0];
    const reader = new FileReader();
    const label = document.getElementById('image-preview-label');

    label.innerText = truncateFileName(file['name']);
    
    /**
     * Display the image in the preview and zoomed image.
     * @param {*} event 
     */
    reader.onload = function(event) {
        const imageUrl = event.target.result;
        const zoomed_image = document.getElementById('zoomed-image');
        const image = document.getElementById('image-preview');

        image.src = imageUrl;
        zoomed_image.src = imageUrl;
        image.classList.add("image-preview-small");
    };
    reader.readAsDataURL(file);
}


/**
 * Show zoomed image.
 */
function toggleZoom() {
    const image = document.getElementById('zoomed-image');
    if (image.hidden) {
        image.hidden = false;
        image.classList.add('zoom');
    }
    else {
        image.hidden = true;
        image.classList.remove('zoom');
    }
}


/**
 * Truncate the file name to 20 characters.
 * @param {string} name 
 * @param {int} length 
 * @returns 
 */
function truncateFileName(name, length=36) {
    if (name.length >= length) {
        const words = name.split('')
        return words.slice(0, length / 4).join('') + '...' + words.slice(-(length / 4)).join('');
    }
    return name;
}


/**
 * Check if the source and target language are the same.
 */
function checkLanguageSelection() {
    let srcLanguage = document.getElementById('src-language');
    let tgtLanguage = document.getElementById('tgt-language');
    if (srcLanguage.value === tgtLanguage.value) {
        alert('Please select different languages for source and target language.');
    }
}
