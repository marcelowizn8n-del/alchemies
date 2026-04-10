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
const apiMeta = document.querySelector('meta[name="alchemies-api-base-url"]');
const apiStatus = document.querySelector("[data-api-status]");
const generateButton = document.querySelector("[data-generate]");
const generateLabel = document.querySelector("[data-generate-label]");
const jobFeedback = document.querySelector("[data-job-feedback]");
const previewTitle = document.querySelector("[data-preview-title]");
const previewMessage = document.querySelector("[data-preview-message]");
const openGenerationLink = document.querySelector("[data-open-generation]");

const progressTitle = document.querySelector("[data-progress-title]");
const progressSubtitle = document.querySelector("[data-progress-subtitle]");
const progressPrimaryName = document.querySelector("[data-progress-primary-name]");
const progressPrimaryDetail = document.querySelector("[data-progress-primary-detail]");
const progressPrimaryState = document.querySelector("[data-progress-primary-state]");
const progressSecondaryName = document.querySelector("[data-progress-secondary-name]");
const progressSecondaryDetail = document.querySelector("[data-progress-secondary-detail]");
const progressSecondaryState = document.querySelector("[data-progress-secondary-state]");
const progressTertiaryName = document.querySelector("[data-progress-tertiary-name]");
const progressTertiaryDetail = document.querySelector("[data-progress-tertiary-detail]");
const progressTertiaryState = document.querySelector("[data-progress-tertiary-state]");

const successMessage = document.querySelector("[data-success-message]");
const successPrimaryName = document.querySelector("[data-success-primary-name]");
const successPrimaryDetail = document.querySelector("[data-success-primary-detail]");
const successPrimaryState = document.querySelector("[data-success-primary-state]");
const successSecondaryName = document.querySelector("[data-success-secondary-name]");
const successSecondaryDetail = document.querySelector("[data-success-secondary-detail]");
const successSecondaryState = document.querySelector("[data-success-secondary-state]");
const successTransaction = document.querySelector("[data-success-transaction]");

const studioState = {
  apiBaseUrl: resolveApiBaseUrl(),
  selectedMode: "image",
  activeRatio: "1:1",
  activeJob: null,
  activeGeneration: null,
  pollTimer: null,
  apiHealthy: false,
};

function resolveApiBaseUrl() {
  const configured = apiMeta?.content?.trim();
  const isLocalContext =
    window.location.protocol === "file:" || ["127.0.0.1", "localhost"].includes(window.location.hostname);

  if (configured && configured !== "/api") {
    return configured.replace(/\/$/, "");
  }

  if (isLocalContext) {
    return "http://127.0.0.1:8000";
  }

  if (configured) {
    return new URL(configured, window.location.origin).toString().replace(/\/$/, "");
  }

  return "http://127.0.0.1:8000";
}

function apiUrl(path) {
  return `${studioState.apiBaseUrl}${path}`;
}

function setApiBadge(message, tone) {
  if (!apiStatus) return;
  apiStatus.textContent = message;
  apiStatus.classList.remove("api-badge-pending", "api-badge-online", "api-badge-offline");
  apiStatus.classList.add(`api-badge-${tone}`);
}

function setJobFeedback(title, detail, tone = "pending") {
  if (!jobFeedback) return;
  const heading = jobFeedback.querySelector("strong");
  const body = jobFeedback.querySelector("span");
  if (heading) heading.textContent = title;
  if (body) body.textContent = detail;
  jobFeedback.classList.remove("is-online", "is-error");
  if (tone === "online" || tone === "success") jobFeedback.classList.add("is-online");
  if (tone === "error") jobFeedback.classList.add("is-error");
}

function setPreviewCopy(title, detail) {
  if (previewTitle) previewTitle.textContent = title;
  if (previewMessage) previewMessage.textContent = detail;
}

function setGenerateBusy(isBusy) {
  if (!generateButton) return;
  generateButton.disabled = isBusy;
  if (generateLabel) {
    generateLabel.textContent = isBusy ? "Dispatching to Own API..." : "Generate Artifact";
  }
}

async function checkApiHealth() {
  if (!apiStatus) return;

  setApiBadge("API status: checking", "pending");

  try {
    const response = await fetch(apiUrl("/healthz"));
    if (!response.ok) throw new Error(`health check failed with ${response.status}`);
    const payload = await response.json();
    studioState.apiHealthy = true;
    setApiBadge(`API online: ${payload.env}`, "online");
    setJobFeedback(
      "Own API connected",
      "The studio is now sending generation jobs to your backend instead of a frontend-only mock.",
      "online",
    );
    setPreviewCopy(
      "Own API ready",
      "The next generation will create a job in your backend, poll for updates, and return artifacts from the orchestration layer.",
    );
  } catch (error) {
    studioState.apiHealthy = false;
    setApiBadge("API offline", "offline");
    setJobFeedback(
      "Own API offline",
      "Start the FastAPI service on port 8000 or configure a reverse proxy at /api before dispatching jobs.",
      "error",
    );
  }
}

if (segmented) {
  const buttons = Array.from(segmented.querySelectorAll("button"));

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      const isVideo = button.dataset.value === "video";
      studioState.selectedMode = isVideo ? "video" : "image";

      if (modelReadout) {
        modelReadout.textContent = isVideo
          ? "Wan 2.1 • Video Worker Planned"
          : "SD 3.5 Large • Image Worker Planned";
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
      studioState.activeRatio = button.dataset.ratio;
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

const closeModals = () => {
  if (studioState.pollTimer) {
    window.clearInterval(studioState.pollTimer);
    studioState.pollTimer = null;
  }
  if (backdrop) backdrop.hidden = true;
  if (progressModal) progressModal.hidden = true;
  if (successModal) successModal.hidden = true;
};

const showSuccess = () => {
  if (progressModal) progressModal.hidden = true;
  if (successModal) successModal.hidden = false;
};

function buildAspectDimensions(ratio) {
  if (ratio === "16:9") return { width: 1280, height: 720 };
  if (ratio === "9:16") return { width: 720, height: 1280 };
  return { width: 1024, height: 1024 };
}

function collectPayload() {
  const prompt = document.querySelector("#positivePrompt")?.value.trim() || "";
  const negativePrompt = document.querySelector("#negativePrompt")?.value.trim() || "";
  const durationSeconds = Number(durationInput?.value || 5);
  const qualityPreset = document.querySelector("#qualityPreset")?.value || "Hyper-Realistic (4K)";
  const { width, height } = buildAspectDimensions(studioState.activeRatio);
  const referenceAssets = uploadInput?.files?.[0]
    ? [{ kind: "image", uri: `upload://${uploadInput.files[0].name}` }]
    : [];

  return {
    prompt,
    negativePrompt,
    durationSeconds,
    width,
    height,
    qualityPreset,
    referenceAssets,
  };
}

function updateProgressModal(job, generation) {
  if (!backdrop || !progressModal || !progressValue || !progressBar) return;

  backdrop.hidden = false;
  progressModal.hidden = false;
  successModal.hidden = true;

  const modeLabel = generation.kind === "video" ? "Video job" : "Image job";
  if (progressTitle) progressTitle.textContent = `Dispatching ${modeLabel}`;
  if (progressSubtitle) progressSubtitle.textContent = job.message;
  progressValue.textContent = `${job.progress}%`;
  progressBar.style.width = `${job.progress}%`;

  if (progressPrimaryName) progressPrimaryName.textContent = `Job ${job.id}`;
  if (progressPrimaryDetail) progressPrimaryDetail.textContent = `Generation ${generation.id}`;
  if (progressPrimaryState) progressPrimaryState.textContent = job.status;

  if (progressSecondaryName) progressSecondaryName.textContent = generation.model;
  if (progressSecondaryDetail) progressSecondaryDetail.textContent = `${generation.kind} orchestration`;
  if (progressSecondaryState) progressSecondaryState.textContent = `${job.progress}%`;

  if (progressTertiaryName) progressTertiaryName.textContent = "Prompt package";
  if (progressTertiaryDetail) {
    progressTertiaryDetail.textContent =
      generation.prompt.length > 72 ? `${generation.prompt.slice(0, 72)}...` : generation.prompt;
  }
  if (progressTertiaryState) progressTertiaryState.textContent = job.status === "queued" ? "Ready" : "Running";
}

function updateSuccessModal(generation) {
  const artifacts = generation.artifacts || [];
  const primaryArtifact = artifacts[0];
  const secondaryArtifact = artifacts[1];

  if (successMessage) {
    successMessage.textContent =
      generation.kind === "video"
        ? "Your own API scaffold completed the video job and registered mock artifact records."
        : "Your own API scaffold completed the image job and registered mock artifact records.";
  }

  if (successPrimaryName) successPrimaryName.textContent = primaryArtifact?.filename || `${generation.id}.bin`;
  if (successPrimaryDetail) successPrimaryDetail.textContent = primaryArtifact?.media_type || "Primary artifact record";
  if (successPrimaryState) successPrimaryState.textContent = "Mock";

  if (successSecondaryName) successSecondaryName.textContent = secondaryArtifact?.filename || `${generation.id}.json`;
  if (successSecondaryDetail) successSecondaryDetail.textContent = secondaryArtifact?.media_type || "Metadata record";
  if (successSecondaryState) successSecondaryState.textContent = "Mock";

  if (successTransaction) successTransaction.textContent = `Generation ID: ${generation.id}`;
  if (openGenerationLink) {
    openGenerationLink.href = apiUrl(`/v1/generations/${generation.id}`);
    openGenerationLink.textContent = "Open Generation";
  }
}

async function fetchJson(path, options = {}) {
  const response = await fetch(apiUrl(path), {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `request failed with ${response.status}`);
  }

  return response.json();
}

async function fetchGeneration(generationId) {
  return fetchJson(`/v1/generations/${generationId}`);
}

async function pollJob(jobId, generationId) {
  if (studioState.pollTimer) {
    window.clearInterval(studioState.pollTimer);
  }

  studioState.pollTimer = window.setInterval(async () => {
    try {
      const job = await fetchJson(`/v1/jobs/${jobId}`);
      const generation = await fetchGeneration(generationId);
      studioState.activeJob = job;
      studioState.activeGeneration = generation;
      updateProgressModal(job, generation);
      setPreviewCopy(
        `Job ${job.status}`,
        `${generation.kind} generation ${generation.id} is being tracked by your own API with ${job.progress}% completion.`,
      );
      setJobFeedback(`Job ${job.status}`, job.message, "online");

      if (job.status === "succeeded") {
        window.clearInterval(studioState.pollTimer);
        studioState.pollTimer = null;
        updateSuccessModal(generation);
        showSuccess();
        setGenerateBusy(false);
        setPreviewCopy(
          "Generation completed",
          `Your own API finished the ${generation.kind} request and stored artifact metadata for ${generation.id}.`,
        );
      }

      if (job.status === "failed") {
        window.clearInterval(studioState.pollTimer);
        studioState.pollTimer = null;
        setGenerateBusy(false);
        closeModals();
        setJobFeedback("Job failed", "The API reported a failed job state. Check the backend logs before retrying.", "error");
      }
    } catch (error) {
      window.clearInterval(studioState.pollTimer);
      studioState.pollTimer = null;
      setGenerateBusy(false);
      closeModals();
      setJobFeedback(
        "Polling interrupted",
        "The studio could not retrieve the latest job status from your API. Verify that the backend is still running.",
        "error",
      );
    }
  }, 900);
}

async function submitGeneration() {
  const payload = collectPayload();

  if (!payload.prompt) {
    setJobFeedback("Prompt required", "Add a positive prompt before dispatching a generation job.", "error");
    return;
  }

  setGenerateBusy(true);
  closeModals();
  setJobFeedback("Dispatching job", "Sending the request to your own API and waiting for orchestration.", "online");
  setPreviewCopy("Dispatching to own API", "Creating a generation job and waiting for the first status update.");

  try {
    const requestBody =
      studioState.selectedMode === "video"
        ? {
            prompt: payload.prompt,
            negative_prompt: payload.negativePrompt,
            model: "wan2.1-t2v-1.3b",
            duration_seconds: payload.durationSeconds,
            aspect_ratio: studioState.activeRatio,
            fps: 16,
            reference_assets: payload.referenceAssets,
            metadata: {
              source: "studio",
              quality_preset: payload.qualityPreset,
            },
          }
        : {
            prompt: payload.prompt,
            negative_prompt: payload.negativePrompt,
            model: "sd3.5-large",
            width: payload.width,
            height: payload.height,
            guidance_scale: 6.5,
            num_inference_steps: payload.qualityPreset === "Fast Preview" ? 18 : 30,
            reference_assets: payload.referenceAssets,
            metadata: {
              source: "studio",
              quality_preset: payload.qualityPreset,
              aspect_ratio: studioState.activeRatio,
            },
          };

    const response = await fetchJson(
      studioState.selectedMode === "video" ? "/v1/generations/video" : "/v1/generations/image",
      {
        method: "POST",
        body: JSON.stringify(requestBody),
      },
    );

    studioState.activeJob = response.job;
    studioState.activeGeneration = response.generation;
    updateProgressModal(response.job, response.generation);
    await pollJob(response.job.id, response.generation.id);
  } catch (error) {
    setGenerateBusy(false);
    closeModals();
    setJobFeedback(
      "API request failed",
      `The studio could not create a generation job. Confirm the backend is reachable at ${studioState.apiBaseUrl}.`,
      "error",
    );
    setPreviewCopy("API request failed", "The frontend could not reach your orchestration layer. Start the API and try again.");
  }
}

document.querySelector("[data-show-progress]")?.addEventListener("click", submitGeneration);
generateButton?.addEventListener("click", submitGeneration);

document.querySelectorAll("[data-close-modals]").forEach((button) => {
  button.addEventListener("click", closeModals);
});

if (backdrop) {
  backdrop.addEventListener("click", closeModals);
}

checkApiHealth();
