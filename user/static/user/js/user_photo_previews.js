const imageInput = document.querySelector("#image-input");
const imagePreview = document.querySelector("#image-preview");
const defaultUserImage = document.querySelector("#image-preview").src;

imageInput.addEventListener("change", (event) => {
    const fileObject = imageInput.files[0];
    if (fileObject) {
        if (fileObject.type.split("/")[0] === "image") {
            const objectURL = URL.createObjectURL(fileObject);
            imagePreview.setAttribute("src", objectURL);
        } else {
            imagePreview.setAttribute("src", defaultUserImage);
        };
    };
});