document.addEventListener("DOMContentLoaded", () => {
  handleToggle("toggle-feed", "feed")
  setupCache()

  function handleImageError() {
    if (imagePlaceholder) {
      this.src = imagePlaceholder
    }
  }

  function handleToggle(buttonId, containerId) {
    const button = document.getElementById(buttonId)
    const container = document.getElementById(containerId)

    if (button && container) {
      button.addEventListener("click", () => {
        container.classList.toggle("hidden")
      })
    }
  }

  function loadImageAndCache(imageId, imageSrc, imageUrl) {
    const img = new Image()
    img.setAttribute("data-type", "image")
    img.onload = () => {
      let item = localStorage.getItem(imageId)

      if (!item) {
        localStorage.setItem(imageId, imageSrc)
        if (navigator.serviceWorker.controller) {
          navigator.serviceWorker.controller.postMessage({
            action: "cache-image",
            imageId: imageId,
            imageSrc: imageSrc,
            imageUrl: imageUrl,
          })
        }
      }
    }

    img.onerror = function () {
      handleImageError.call(this)
    }
    img.src = imageSrc
  }

  function setupCache() {
    let cachedImageUrls = {}

    const images = document.querySelectorAll("[data-type=image]")
    if (images) {
      images.forEach((image) => {
        const imageId = image.alt
        const imageSrc = image.src
        const storedData = localStorage.getItem(imageId)

        if (storedData) {
          cachedImageUrls[imageId] = storedData
          cachedImageUrls[imageSrc] = imageSrc
        } else {
          cachedImageUrls[imageId] = ""
          cachedImageUrls[imageSrc] = ""
        }

        if (image.src && image.src !== imagePlaceholder) {
          image.onerror = handleImageError
        }
        loadImageAndCache(imageId, image.src, cachedImageUrls)
      })
    }
  }
})
