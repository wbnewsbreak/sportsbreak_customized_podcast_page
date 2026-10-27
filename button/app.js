const ANALYTICS_URL = "https://script.google.com/macros/s/AKfycbzVl1Yuy6G75C0ObZgx7aXtEcCYs8i-0P11xniruh_JKfhtIK9kdZg2FBb_LM5UqvG7Ow/exec";

const DEFAULT_LEAGUES = ["nfl", "mlb", "cfb", "nba"];
const HEARTBEAT_INTERVAL_SECONDS = 15;
const PLAY_LABEL = "Play Your AI-generated Daily Briefing";
const PAUSE_LABEL = "Pause";

const params = new URLSearchParams(window.location.search);
const userId = params.get("firebase_uid") || "anonymous";
let leagues = DEFAULT_LEAGUES;
const playButton = document.querySelector("#play-button");
const status = document.querySelector("#status");
const audio = document.querySelector("#audio");

let currentLeagueIndex = 0;
let hasStartedCurrentLeague = false;
let nextHeartbeatAt = HEARTBEAT_INTERVAL_SECONDS;
let isPlaying = false;

function episodeDate() {
  return new Date().toISOString().slice(0, 10);
}

function completionPercent(currentTime = audio.currentTime) {
  if (!Number.isFinite(audio.duration) || audio.duration <= 0) {
    return 0;
  }

  return Math.min(100, Math.round((currentTime / audio.duration) * 100));
}

async function postAnalytics(payload) {
  try {
    await fetch(ANALYTICS_URL, {
      method: "POST",
      mode: "no-cors",
      redirect: "follow",
      headers: { "Content-Type": "text/plain;charset=UTF-8" },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    console.error("Unable to send briefing analytics:", error);
  }
}

function sendAnalytics(currentTime = audio.currentTime, isComplete = false) {
  postAnalytics({
    user: userId,
    league: leagues[currentLeagueIndex],
    completionPercent: isComplete ? 100 : completionPercent(currentTime),
  });
}

function logImpression() {
  postAnalytics({ user: userId, league: "sawPodcast" });
}

document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "visible") {
    logImpression();
  }
});

if (document.visibilityState === "visible") {
  logImpression();
}

function loadCurrentLeague() {
  const league = leagues[currentLeagueIndex];
  const date = episodeDate();
  audio.src = `https://archive.org/download/sportsbreak-${date}/${encodeURIComponent(league)}.mp3`;
  audio.load();
  hasStartedCurrentLeague = false;
  nextHeartbeatAt = HEARTBEAT_INTERVAL_SECONDS;
}

function showError(message) {
  status.textContent = message;
}

playButton.addEventListener("click", async () => {
  showError("");

  if (isPlaying) {
    audio.pause();
    return;
  }

  if (currentLeagueIndex >= leagues.length) {
    currentLeagueIndex = 0;
    loadCurrentLeague();
  }

  try {
    await audio.play();
  } catch (error) {
    showError("Unable to play the briefing. Please try again.");
    console.error("Audio playback failed:", error);
  }
});

audio.addEventListener("play", () => {
  isPlaying = true;
  playButton.textContent = PAUSE_LABEL;

  if (!hasStartedCurrentLeague) {
    hasStartedCurrentLeague = true;
    sendAnalytics();
  }
});

audio.addEventListener("pause", () => {
  isPlaying = false;
  playButton.textContent = PLAY_LABEL;
});

audio.addEventListener("timeupdate", () => {
  while (audio.currentTime >= nextHeartbeatAt) {
    sendAnalytics(nextHeartbeatAt);
    nextHeartbeatAt += HEARTBEAT_INTERVAL_SECONDS;
  }
});

audio.addEventListener("ended", () => {
  sendAnalytics(audio.duration, true);
  currentLeagueIndex += 1;

  if (currentLeagueIndex < leagues.length) {
    loadCurrentLeague();
    audio.play().catch((error) => {
      showError("Unable to play the next briefing. Please try again.");
      console.error("Next audio playback failed:", error);
    });
    return;
  }

  isPlaying = false;
  playButton.textContent = PLAY_LABEL;
});

audio.addEventListener("error", () => {
  isPlaying = false;
  playButton.textContent = PLAY_LABEL;
  showError(`The ${leagues[currentLeagueIndex]} briefing could not be loaded.`);
});

const userLeagues = window.FIREBASE_UID_TO_LEAGUES;
const configuredLeagues = userLeagues?.[userId];
if (
  Array.isArray(configuredLeagues) &&
  configuredLeagues.length > 0 &&
  configuredLeagues.every((league) => typeof league === "string")
) {
  leagues = configuredLeagues;
}

playButton.disabled = false;
loadCurrentLeague();
