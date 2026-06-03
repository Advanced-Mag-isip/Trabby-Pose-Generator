const BASE_URL = `${import.meta.env.INTERNAL_API_URL || import.meta.env.PUBLIC_API_URL}/api`;/* ---------------------------------------
   SAFE FETCH (SSR-safe + JSON-safe)
---------------------------------------- */


async function safeFetch(url) {
  const res = await fetch(url);
  const text = await res.text();
  if (!res.ok) {
    console.error("API ERROR:", url, text);
    throw new Error(`HTTP ${res.status} at ${url}`);
  }

  try {
    return JSON.parse(text);
  } catch (err) {
    console.error("INVALID JSON RESPONSE:", url, text);
    throw err;
  }
}

// Pose Generation Metrics
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

// Pose Selection Metrics
export function getTotalPoseSelections() {
  return safeFetch(`${BASE_URL}/poses/selectionTotal/`);
}

export function getSelectionPerPose() {
  return safeFetch(`${BASE_URL}/poses/selectionPerPose/`);
}

export function getTopPoseRanking() {
  return safeFetch(`${BASE_URL}/poses/topConfigurations`);
}

// Export-related metrics
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

export function getMostUsedAsset() {
  return safeFetch(`${BASE_URL}/exports/assets/mostUsed/`);
}