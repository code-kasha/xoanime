document.addEventListener("DOMContentLoaded", function () {
  const video = document.getElementById("video")

  initializeHLS()
  playerActions()
  toggleServer()

  function changeQuality(quality) {
    if (window.hls) {
      window.hls.levels.forEach((level, levelIndex) => {
        if (level.height === quality) {
          window.hls.currentLevel = levelIndex
        }
      })
    }
  }

  function getPlaybackPosition() {
    return localStorage.getItem(`${nowPlaying}-time`) || 0
  }

  function initializeHLS() {
    const options = {
      controls: [
        "restart",
        "rewind",
        "play",
        "fast-forward",
        "mute",
        "volume",
        "progress",
        "current-time",
        "duration",
        "settings",
        "pip",
        "airplay",
        "fullscreen",
      ],
      autoplay: true,
    }

    if (Hls.isSupported()) {
      const hls = new Hls()
      hls.loadSource(
        document.getElementById("default-source").getAttribute("src")
      )

      video.currentTime = getPlaybackPosition()

      hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
        const availableQualities = hls.levels.map((l) => l.height)
        const defaultQuality = Math.max.apply(null, availableQualities)
        options.quality = {
          default: defaultQuality,
          options: availableQualities,
          forced: true,
          onChange: (e) => changeQuality(e),
        }
        new Plyr(video, options)
      })

      hls.attachMedia(video)
      window.hls = hls
    }

    video.addEventListener("play", () => {
      video.setAttribute("tabindex", "0")
      video.focus()
    })

    video.addEventListener("timeupdate", function () {
      setPlaybackPosition(video.currentTime)
    })
  }

  function playerActions() {
    const previousEpisode = document.getElementById("previous-episode")
    const nextEpisode = document.getElementById("next-episode")

    document.addEventListener("keyup", (event) => {
      if (event.shiftKey) {
        switch (event.key) {
          case "ArrowLeft":
            previousEpisode.click()
            break
          case "ArrowRight":
            nextEpisode.click()
            break
        }
      }
    })
  }

  function setPlaybackPosition(position) {
    localStorage.setItem(`${nowPlaying}-time`, position)
  }

  function toggleServer() {
    const button = document.getElementById("change-source")

    if (button) {
      button.addEventListener("click", () => {
        changeSource()
      })
    }
  }
})
