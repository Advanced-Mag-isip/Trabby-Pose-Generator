const BASE_URL = "http://127.0.0.1:8000/api";

/* ---------------------------------------
   SAFE FETCH (SSR-safe + JSON-safe)
---------------------------------------- */
async function safeFetch(url) {
  const res = await fetch(url);
  const text = await res.text();

  // Handle HTTP errors
  if (!res.ok) {
    console.error("API ERROR:", url, text);
    throw new Error(`HTTP ${res.status} at ${url}`);
  }

  // Ensure valid JSON
  try {
    return JSON.parse(text);
  } catch (err) {
    console.error("INVALID JSON RESPONSE:", url, text);
    throw err;
  }
}

/* =======================================
   POSE GENERATION METRICS
======================================= */

export function getPoseGenerationRate() {
  return safeFetch(`${BASE_URL}/poses/generationRate/`);
}

export function getPredefinedPoseCount() {
  return safeFetch(`${BASE_URL}/poses/predefined/`);
}

export function getCustomizedPoseCount() {
  return safeFetch(`${BASE_URL}/poses/customized/`);
}

export function getTotalPoseCount() {
  return safeFetch(`${BASE_URL}/poses/totalGenerated/`);
}

/* =======================================
   POSE USAGE METRICS
======================================= */

export function getTotalPoseSelections() {
  return safeFetch(`${BASE_URL}/poses/selectionTotal/`);
}

export function getSelectionPerPose() {
  return safeFetch(`${BASE_URL}/poses/selectionPerPose/`);
}

export function getTopPoseRanking() {
  return safeFetch(`${BASE_URL}/poses/topPoses/`);
}

/* =======================================
   EXPORT METRICS
======================================= */

export function getTotalExports() {
  return safeFetch(`${BASE_URL}/exports/total/`);
}

export function getExportsPerPose(poseId) {
  return safeFetch(`${BASE_URL}/exports/pose/${poseId}/`);
}

export function getExportsPerMonth() {
  return safeFetch(`${BASE_URL}/exports/month/`);
}

export function getTopExports() {
  return safeFetch(`${BASE_URL}/exports/pose/`);
}