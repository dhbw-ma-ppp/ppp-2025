/* ---------------------- Deine Bildlisten ---------------------- */
/* Passe die Dateinamen/Pfade an. Bilder sollten im gleichen Ordner oder per Pfad erreichbar sein. */
const phishingImages = [
  "chef-154396_1280.png",
  "dead_fish.png",
  "angry_fish.png",
];

const safeImages = ["4250480-1.jpg", "happy_star.png", "thumbs_up.png"];

/* ---------------------- Popup-Funktion ---------------------- */
function showPopup(message, images) {
  const popup = document.createElement("div");
  popup.classList.add("popup");

  const img = images[Math.floor(Math.random() * images.length)];

  popup.innerHTML = `
    <h2>${message}</h2>
    <img src="${img}" alt="Popup Bild">
    <br>
    <button id="closePopup">OK</button>
  `;

  document.body.appendChild(popup);

  document.getElementById("closePopup").addEventListener("click", () => {
    popup.remove();
  });
}

/* ---------------------- Fish Animation ---------------------- */
function startFishAnimation() {
  const anim = document.getElementById("fishAnimation");
  anim.classList.add("animation-start");

  // zurücksetzen, damit man die Animation später wieder abspielen kann
  setTimeout(() => anim.classList.remove("animation-start"), 4000);
}

/* ---------------------- Formular-Handler ---------------------- */
document
  .getElementById("phishForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    startFishAnimation();

    const subject = document.getElementById("subjectField").value.trim();
    const email = document.getElementById("mailField").value.trim();

    /* ----------------------------
     HIER verbindest du DEIN Backend
     Beispiel (Flask/FastAPI) POST an /predict:
  ----------------------------- */
    /*
  try {
    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject, email })
    });
    const data = await res.json();

    // Beispiel: backend liefert { prediction: "phishing", confidence: 0.92 }
    if (data.prediction === "phishing") {
      showPopup("⚠️ You are cooked like a fish!", phishingImages);
    } else {
      showPopup("🟢 The mail is valid!", safeImages);
    }
    return;
  } catch (err) {
    console.error("Fehler beim Abrufen der API:", err);
    showPopup("Fehler: Backend nicht erreichbar", safeImages);
    return;
  }
  */

    // Fallback Dummy (wenn Backend noch nicht läuft)
    setTimeout(() => {
      const isPhish = Math.random() > 0.5;
      if (isPhish) {
        showPopup("⚠️ You are cooked like a fish!", phishingImages);
      } else {
        showPopup("🟢 The mail is valid!", safeImages);
      }
    }, 1200);
  });
