// god-eye.js - Cesium 3D Globe with Google Photorealistic Tiles
import * as Cesium from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';

// Your Cesium Ion access token
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyMzg4ODRiMS05MTg2LTQ3ZWUtODdkYS1iMWI1NDQ2N2Y0ZGIiLCJpZCI6NDAzMTAxLCJpYXQiOjE3NzM0MDkzODl9.r_yNdcbiwZUpdLpl4bkxktmEq_1ZzDmjkZVRK2jDeJw';

// Initialize the Cesium viewer
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrainProvider: await Cesium.createWorldTerrainAsync(),
  baseLayerPicker: false,
  geocoder: false,
  homeButton: false,
  sceneModePicker: false,
  navigationHelpButton: false,
  animation: false,
  timeline: false,
  fullscreenButton: false,
  infoBox: false,
  selectionIndicator: false,
  targetFrameRate: 60,
  contextOptions: {
    webgl: {
      alpha: true,
      preserveDrawingBuffer: true
    }
  }
});

// Add Google Photorealistic 3D Tiles
try {
  const googleTileset = await Cesium.Cesium3DTileset.fromIonAssetId(2275207); // Google Photorealistic 3D Tiles asset ID
  viewer.scene.primitives.add(googleTileset);
  console.log('✅ Google 3D Tiles loaded');
} catch (error) {
  console.error('Failed to load Google 3D Tiles:', error);
}

// Remove default sky atmosphere and stars for cleaner look
viewer.scene.skyAtmosphere.show = false;
viewer.scene.skyBox.show = false;

// Customize lighting
viewer.scene.globe.enableLighting = true;
viewer.scene.globe.dynamicAtmosphereLighting = true;
viewer.scene.globe.dynamicAtmosphereLightingFromSun = true;

// Set initial view to a dramatic angle
viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(-74.006, 40.7128, 1000), // NYC
  orientation: {
    heading: Cesium.Math.toRadians(20),
    pitch: Cesium.Math.toRadians(-35),
    roll: 0
  },
  duration: 2
});

// Add a simple HUD overlay
const hud = document.createElement('div');
hud.style.position = 'absolute';
hud.style.top = '20px';
hud.style.left = '20px';
hud.style.color = '#0f0';
hud.style.fontFamily = 'monospace';
hud.style.fontSize = '14px';
hud.style.zIndex = '1000';
hud.style.textShadow = '0 0 10px #0f0';
hud.innerHTML = '🛰️ GOD-EYE OS<br>⚡ REAL-TIME GEOSPATIAL INTELLIGENCE';
document.body.appendChild(hud);

// Add FPS counter
let lastTime = performance.now();
let frames = 0;
const fpsCounter = document.createElement('div');
fpsCounter.style.position = 'absolute';
fpsCounter.style.bottom = '20px';
fpsCounter.style.right = '20px';
fpsCounter.style.color = '#0f0';
fpsCounter.style.fontFamily = 'monospace';
fpsCounter.style.fontSize = '12px';
fpsCounter.style.zIndex = '1000';
fpsCounter.style.textShadow = '0 0 5px #0f0';
document.body.appendChild(fpsCounter);

function updateFPS() {
  frames++;
  const now = performance.now();
  const delta = now - lastTime;
  if (delta >= 1000) {
    const fps = Math.round((frames * 1000) / delta);
    fpsCounter.innerHTML = `📊 FPS: ${fps}`;
    frames = 0;
    lastTime = now;
  }
  requestAnimationFrame(updateFPS);
}
updateFPS();

// Handle window resize
window.addEventListener('resize', () => {
  viewer.resize();
});

console.log('✅ God-Eye OS Cesium initialized');