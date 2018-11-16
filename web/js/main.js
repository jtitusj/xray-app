const image1 = document.querySelector('#image1');
const image2 = document.querySelector('#image2');
const loader = document.querySelector('.loader');
const filename = document.querySelector('.file-name');
const subtext = document.querySelector('#subtext');
const inputimgupload = document.querySelector('#img-upload');
const loadingmodel = document.querySelector('#loading-model');
const learnmore = document.querySelector('.learn-more-text');
const learnmorecontent = document.querySelector('.learn-more-content');
const fileinput = document.querySelector('.file-input');
// const btnloadmodel = document.querySelector('#btn-load-model');

// btnloadmodel.addEventListener('click', function(e) {
//     btnloadmodel.disabled = true;
//     fetch('/init_model', {method: 'GET'}).then(
//         function(response) {
//             return response.text();
//         }
//     ).then(function(result) {
//         if (result=='True') {
//             console.log('Model loaded');
//             // inputimgupload.disabled = false
            
//             btnloadmodel.setAttribute('style', 'display: none;');
//             inputimgupload.setAttribute('style', 'display: inline-block;');
//         }
//     })
// })


learnmore.addEventListener('click', function(e) {
    learnmore.setAttribute('style', 'display: none;');
    learnmorecontent.setAttribute('style', 'display: block;');
})

fetch('/init_model', {method: 'GET'}).then(
    function(response) {
        return response.text();
    }
).then(function(result) {
    if (result=='True') {
        console.log('Model loaded');
        loadingmodel.setAttribute('style', 'display: none;')
        inputimgupload.setAttribute('style', 'display: inline-block;');

        image1.addEventListener('click', function(e) {
            fileinput.click();
        })
    }
})

function process_image(b64_image) {
    fetch('/process_image', {
        method: 'POST',
        body: b64_image
    }).then(
    function(response) {
        return response.json();
    }).then(function(result) {
        // console.log(result)
        label = result['label'];
        prob = parseFloat(result['prob']).toFixed(2);
        // subtext.textContent = "ChexNet 121-layer CNN: "+prob+"% "+label;

        texts = ["ChexNet 121-layer CNN: ", prob+"% "+label]
        highlights = [false, true]

        subtext.textContent = "";
        
        for (let i=0; i<texts.length; i++) {
            let span = document.createElement('SPAN');
            span.textContent = texts[i];
            if (highlights[i]) {
                span.setAttribute('style', 'color: red;');
            }
            subtext.appendChild(span);
        }

        // subtext.appendChild("ChexNet 121-layer CNN: "+prob+"% "+label);

        img = result['image'];
        const b64_image = "data:image/png;base64,"+img;
        image2.setAttribute('src', b64_image);
        loader.setAttribute('style', 'visibility: hidden;');
    }).catch(function(e) {
        console.log(e);
        loader.setAttribute('style', 'visibility: hidden;');
    });
}

function readURL(input) {
    if (input.files && input.files[0]) {
        file = input.files[0].name;
        filename.textContent = file;
        var reader = new FileReader();
        reader.onload = function (e) {
            // console.log(e.target.result);
            loader.setAttribute('style', 'visibility: visible;');
            image1.setAttribute('src', e.target.result);
            image2.setAttribute('src', 'web/images/placeholder.png');
            process_image(e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}    