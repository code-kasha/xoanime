document.addEventListener("DOMContentLoaded", () => {
  handleToggle("toggle-feed", "feed")
  handleToggle("toggle-chapter-list", "chapter-list")
  handleToggle("sidebar-menu-button", "sidebar-menu")
  handleTruncation()
  readerActions()
  batchEpisodes()
  setupCache()
  scrollIntoView()

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

  function readerActions() {
    const previousChapter = document.getElementById("previous-chapter")
    const nextChapter = document.getElementById("next-chapter")

    document.addEventListener("keyup", (event) => {
      if (event.shiftKey) {
        switch (event.key) {
          case "ArrowLeft":
            previousChapter.click()
            break
          case "ArrowRight":
            nextChapter.click()
            break
          case "ArrowUp":
            break
          case "ArrowDown":
            break
        }
      }
    })
  }

  function batchEpisodes() {
    var select = document.getElementById("groupRange")
    var episodes = document.querySelectorAll(".episode-item")

    if (select) {
      select.addEventListener("change", function () {
        var selectedRange = this.value.split("-")
        var startRange = parseInt(selectedRange[0])
        var endRange = parseInt(selectedRange[1])

        episodes.forEach(function (episode) {
          var episodeNumber = parseInt(episode.dataset.episodeNumber)
          episode.style.display =
            episodeNumber >= startRange && episodeNumber <= endRange
              ? "block"
              : "none"
        })
      })

      select.dispatchEvent(new Event("change"))
    }
  }

  function scrollIntoView() {
    var selectedElement = document.querySelector(
      `[data-episode-id=${selectedItem.id}]`
    )

    if (selectedElement) {
      selectedElement.scrollIntoView({ behavior: "smooth" })
    }
  }

  function handleTruncation() {
    const items = document.querySelectorAll("[data-action=truncate]")
    items.forEach((item) => {
      item.addEventListener("click", () => {
        item.classList.toggle("truncate")
      })
    })
  }
})
