document.addEventListener("astro:page-load", () => {
  console.log("Customization script loaded");

  const downloadBtn = document.getElementById("download-btn");

  if (!downloadBtn) {
    console.error("Download button not found");
    return;
  }

  console.log("Download button found");

  downloadBtn.addEventListener("click", getPoseInfo);
});

async function getPoseInfo(event) {
  event?.preventDefault();

  try {
    const input = document.querySelector(
      ".character-preview-actions input"
    );

    const pose_name = input?.value?.trim() || "Untitled Pose";

    const config = buildPoseConfiguration();

    const payload = {
      pose_name,
      pose: config,
    };

    console.log("Sending payload:", payload);

    const response = await fetch(
       `${import.meta.env.PUBLIC_API_URL}/api/exports/poses/create/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      }
    );

    const contentType = response.headers.get("content-type");

    if (!response.ok) {
      let errorMessage;

      if (contentType?.includes("application/json")) {
        const errorData = await response.json();
        errorMessage = errorData.error || JSON.stringify(errorData);
      } else {
        errorMessage = await response.text();
      }

      console.error("Server Error:", errorMessage);

      throw new Error(
        `HTTP ${response.status}: ${response.statusText}`
      );
    }

    let savedPose;

    if (contentType?.includes("application/json")) {
      savedPose = await response.json();
    } else {
      throw new Error("Expected JSON response from server.");
    }

    console.log("Pose saved successfully:", savedPose);

    if (savedPose.pose_id) {
      console.log("Generated Pose ID:", savedPose.pose_id);
    }

    return savedPose;

  } catch (error) {
    console.error("getPoseInfo error:", error);
  }
}

// Mapping selected assets by their subcategory
function getSelectionMapBySub() {
  const map = new Map();

  const source =
    typeof previewSelections !== "undefined" ? previewSelections : {};

  for (const [sub, entry] of Object.entries(source)) {
    // ONLY keep actual selected items
    if (!entry || !entry.spriteUrl) continue;

    map.set(sub, entry.spriteUrl);
  }

  return map;
}

// Build pose configuration
function buildPoseConfiguration() {
  const selected = getSelectionMapBySub();
  const getAsset = (sub) => selected.get(sub) || null;

  return {
    head: {
      asset: getAsset("Head Position"),
      x: 0,
      y: 0,
      rotation_deg: 0,
      subparts: {
        eyes: { asset: getAsset("Eyes"), x: 0, y: 0, rotation_deg: 0 },
        mouth: { asset: getAsset("Mouth"), x: 0, y: 0, rotation_deg: 0 },
        ears: { asset: getAsset("Ears"), x: 0, y: 0, rotation_deg: 0 },
        hair: { asset: getAsset("Hair"), x: 0, y: 0, rotation_deg: 0 },
        eyebrows: { asset: getAsset("Eyebrows"), x: 0, y: 0, rotation_deg: 0 }
      }
    },

    limbs: {
      asset: getAsset("Limbs"),
      x: 0,
      y: 0,
      rotation_deg: 0,
      subparts: {
        left_upper_arm: { asset: getAsset("Left Upper Arm"), x: 0, y: 0, rotation_deg: 0 },
        right_upper_arm: { asset: getAsset("Right Upper Arm"), x: 0, y: 0, rotation_deg: 0 },
        left_forearm: { asset: getAsset("Left Forearm & Hand"), x: 0, y: 0, rotation_deg: 0 },
        right_forearm: { asset: getAsset("Right Forearm & Hand"), x: 0, y: 0, rotation_deg: 0 },
        left_thigh: { asset: getAsset("Left Thigh"), x: 0, y: 0, rotation_deg: 0 },
        right_thigh: { asset: getAsset("Right Thigh"), x: 0, y: 0, rotation_deg: 0 },
        left_lower_leg: { asset: getAsset("Left Lower Leg & Foot"), x: 0, y: 0, rotation_deg: 0 },
        right_lower_leg: { asset: getAsset("Right Lower Leg & Foot"), x: 0, y: 0, rotation_deg: 0 },
        tail: { asset: getAsset("Tail"), x: 0, y: 0, rotation_deg: 0 }
      }
    },

    torso: {
      asset: getAsset("Torso Shape"),
      x: 0,
      y: 0,
      rotation_deg: 0
    },

    accessories: {
      wearable: {
        asset: getAsset("Wearables"),
        x: 0,
        y: 0,
        rotation_deg: 0
      },
      holdable: {
        asset: getAsset("Holdables"),
        x: 0,
        y: 0,
        rotation_deg: 0
      }
    }
  };
}