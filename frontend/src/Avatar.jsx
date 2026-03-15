import { useRef, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function AudioVisualizer({ isSpeaking, isListening, emotion }) {
  const barsRef = useRef()
  const timeRef = useRef(0)
  const barCount = 64
  const waveData = useRef(new Array(barCount).fill(0.1))
  
  useFrame((state, delta) => {
    timeRef.current += delta
    
    if (barsRef.current) {
      barsRef.current.children.forEach((bar, i) => {
        const normalizedIndex = i / barCount
        let targetHeight = 0.1
        let hue = 0.5
        let saturation = 0.6
        let lightness = 0.4
        
        if (isListening) {
          const wave = Math.sin(timeRef.current * 7 + i * 0.4) * 0.5
          const wave2 = Math.sin(timeRef.current * 5 + i * 0.3) * 0.3
          const noise = Math.random() * 0.2
          targetHeight = wave + wave2 + noise + 0.3
          hue = 0.08 + normalizedIndex * 0.05
          saturation = 1
          lightness = 0.5 + (targetHeight * 0.2)
        }
        else if (isSpeaking) {
          const bass = Math.sin(timeRef.current * 6 + i * 0.2) * 0.4
          const mid = Math.sin(timeRef.current * 9 + i * 0.4) * 0.5
          const high = Math.sin(timeRef.current * 12 + i * 0.6) * 0.3
          const noise = Math.random() * 0.3
          const weight = 1 - normalizedIndex
          targetHeight = (bass * weight) + mid + (high * normalizedIndex) + noise + 0.3
          
          if (emotion.stress > 0.5) {
            hue = 0.95 + normalizedIndex * 0.03
            saturation = 1
          } else if (emotion.confidence > 0.7) {
            hue = 0.5 + normalizedIndex * 0.08
            saturation = 1
          } else if (emotion.curiosity > 0.6) {
            hue = 0.75 + normalizedIndex * 0.05
            saturation = 1
          } else {
            hue = 0.3 + normalizedIndex * 0.08
            saturation = 0.9
          }
          lightness = 0.5 + (targetHeight * 0.2)
        }
        else {
          const breathe = Math.sin(timeRef.current * 1.5 + i * 0.15) * 0.03
          targetHeight = 0.1 + breathe
          hue = 0.5 + normalizedIndex * 0.03
          saturation = 0.4
          lightness = 0.3
        }
        
        waveData.current[i] += (targetHeight - waveData.current[i]) * 0.2
        bar.scale.y = THREE.MathUtils.lerp(bar.scale.y, waveData.current[i], 0.3)
        
        const targetColor = new THREE.Color().setHSL(hue, saturation, lightness)
        bar.material.color.lerp(targetColor, 0.15)
        
        const targetEmissive = new THREE.Color().setHSL(hue, saturation * 0.7, lightness * 0.6)
        bar.material.emissive.lerp(targetEmissive, 0.15)
        bar.material.emissiveIntensity = waveData.current[i] * 0.8
      })
    }
  })
  
  return (
    <group ref={barsRef} position={[0, -0.5, 0]}>
      {Array.from({ length: barCount }).map((_, i) => (
        <mesh key={i} position={[(i - barCount / 2) * 0.13, 0, 0]}>
          <boxGeometry args={[0.1, 1, 0.1]} />
          <meshStandardMaterial emissive="#00f0ff" emissiveIntensity={0.5} roughness={0.3} metalness={0.8} transparent opacity={0.95} />
        </mesh>
      ))}
    </group>
  )
}

export default function Avatar({ emotion, isSpeaking, isListening }) {
  return (
    <div className="avatar-container">
      <Canvas camera={{ position: [0, 0, 4], fov: 50 }} gl={{ antialias: true }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[10, 10, 10]} intensity={1} />
        <pointLight position={[-10, -5, -5]} intensity={0.5} color="#bc13fe" />
        <AudioVisualizer isSpeaking={isSpeaking} isListening={isListening} emotion={emotion} />
      </Canvas>
    </div>
  )
}