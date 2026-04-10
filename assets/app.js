const authTabs = document.querySelector("[data-auth-tabs]");
const authForm = document.querySelector(".auth-form");

if (authTabs) {
  const buttons = Array.from(authTabs.querySelectorAll("[data-auth-mode]"));
  const submit = document.querySelector("[data-auth-submit]");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      if (submit) {
        submit.textContent = button.dataset.authMode === "signup" ? "Create Account" : "Sign In";
      }
    });
  });
}

if (authForm) {
  authForm.addEventListener("submit", (event) => {
    event.preventDefault();
    window.location.href = "studio.html";
  });
}

const segmented = document.querySelector("[data-segmented]");
const durationInput = document.querySelector("#durationRange");
const durationReadout = document.querySelector("[data-duration-readout]");
const modelReadout = document.querySelector("[data-model-readout]");

if (segmented) {
  const buttons = Array.from(segmented.querySelectorAll("button"));

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      const isVideo = button.dataset.value === "video";

      if (modelReadout) {
        modelReadout.textContent = isVideo
          ? "Video Diffusion • Temporal Pass Enabled"
          : "Stable Diffusion XL • 45 Steps";
      }
    });
  });
}

if (durationInput && durationReadout) {
  const syncDuration = () => {
    durationReadout.textContent = `${durationInput.value}s`;
  };

  durationInput.addEventListener("input", syncDuration);
  syncDuration();
}

const ratioGroup = document.querySelector("[data-ratios]");
if (ratioGroup) {
  const buttons = Array.from(ratioGroup.querySelectorAll("button"));
  const artifactShell = document.querySelector("[data-artifact-shell]");
  const defaultHeight = artifactShell ? window.getComputedStyle(artifactShell).minHeight : null;

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      if (!artifactShell) return;

      artifactShell.classList.remove("artifact-square");
      if (button.dataset.ratio === "1:1") {
        artifactShell.classList.add("artifact-square");
        artifactShell.style.minHeight = defaultHeight;
      } else if (button.dataset.ratio === "16:9") {
        artifactShell.style.minHeight = "420px";
      } else {
        artifactShell.style.minHeight = "720px";
      }
    });
  });
}

const uploadInput = document.querySelector("#structureRef");
const uploadLabel = document.querySelector("[data-upload-label]");
if (uploadInput && uploadLabel) {
  uploadInput.addEventListener("change", () => {
    const file = uploadInput.files?.[0];
    if (file) uploadLabel.textContent = file.name;
  });
}

const backdrop = document.querySelector("[data-modal-backdrop]");
const progressModal = document.querySelector('[data-modal="progress"]');
const successModal = document.querySelector('[data-modal="success"]');
const progressValue = document.querySelector("[data-progress-value]");
const progressBar = document.querySelector("[data-progress-bar]");
let progressTimer = null;

const closeModals = () => {
  if (progressTimer) {
    window.clearInterval(progressTimer);
    progressTimer = null;
  }
  if (backdrop) backdrop.hidden = true;
  if (progressModal) progressModal.hidden = true;
  if (successModal) successModal.hidden = true;
};

const showSuccess = () => {
  if (progressModal) progressModal.hidden = true;
  if (successModal) successModal.hidden = false;
};

const showProgress = () => {
  closeModals();
  if (!backdrop || !progressModal || !progressValue || !progressBar) return;

  let value = 65;
  backdrop.hidden = false;
  progressModal.hidden = false;
  progressValue.textContent = `${value}%`;
  progressBar.style.width = `${value}%`;

  progressTimer = window.setInterval(() => {
    value += 7;
    progressValue.textContent = `${Math.min(value, 100)}%`;
    progressBar.style.width = `${Math.min(value, 100)}%`;

    if (value >= 100) {
      window.clearInterval(progressTimer);
      progressTimer = null;
      window.setTimeout(showSuccess, 260);
    }
  }, 380);
};

document.querySelectorAll("[data-show-progress], [data-generate]").forEach((button) => {
  button.addEventListener("click", showProgress);
});

document.querySelectorAll("[data-close-modals]").forEach((button) => {
  button.addEventListener("click", closeModals);
});

if (backdrop) {
  backdrop.addEventListener("click", closeModals);
}
