document.addEventListener("DOMContentLoaded", () => {
  toggle("toggle-feed", "feed")

  function toggle(buttonId, containerId) {
    const button = document.getElementById(buttonId)
    const container = document.getElementById(containerId)

    if (button && container) {
      button.addEventListener("click", () => {
        container.classList.toggle("hidden")
      })
    }
  }
})
