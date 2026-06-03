document.addEventListener("DOMContentLoaded", loadGallery);

const LAYER_Z = {
  torso: 10,
  limbs: 20,
  head: 30,
  face: 32,
  body: 37,
  expression: 38,
  wearable: 50,
};

const LAYER_PATHS = {
  torso: ["torso"],
  limbs: ["limbs"],
  head: ["head"],
  face: ["face"],
  body: ["body"],
  expression: ["expression"],
  wearable: ["accessories", "wearable"],
};

async function loadGallery() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/exports/pose/config/");
    const poses = await res.json();

    window.__GRID_DATA__ = poses.map((pose) => ({
      id: pose.id,
      name: pose.name || "Untitled Pose",
      created: pose.created,
      sprites: buildLayers(pose.config).map(({ src, z, type }) => ({
        src,
        z,
        type,
      })),
    }));
    // console.log("GRID DATA:", window.__GRID_DATA__);
    window.__GRID_DATA__.forEach(item => {
      console.log(`Pose ${item.id}: ${item.name}`);

      console.table(
        item.sprites.map(sprite => ({
        z: sprite.z,
        src: sprite.src,
        type: sprite.type}))
      );
    });
  } catch (err) {
    console.error("Failed to load gallery:", err);
  }
}

function buildLayers(config = {}) {
  const layers = [
    ["torso", config.torso?.asset],
    ["limbs", config.limbs?.asset],
    ["head", config.head?.asset],
    ["face", config.face?.asset],
    ["body", config.body?.asset],
    ["expression", config.expression?.asset],
    ["wearable", config.accessories?.wearable?.asset],
  ];

  return layers
    .filter(([, asset]) => asset)
    .map(([type, src]) => ({ src, z: LAYER_Z[type], type }))
    .sort((a, b) => a.z - b.z);
}