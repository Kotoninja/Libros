const imageInput = document.querySelector("#image-input");
const imagePreview = document.querySelector("#image-preview");

imageInput.addEventListener("change", (event) => {
    const fileObject = imageInput.files[0];

    const objectURL = URL.createObjectURL(fileObject);

    imagePreview.setAttribute("src", objectURL)
});