import { useState } from "react"

import { Canvas } from "@react-three/fiber"

import {
  OrbitControls,
  Grid
} from "@react-three/drei"

import STLModel from "./STLModel"


export default function Viewer() {

  const [reloadKey, setReloadKey] =
    useState(Date.now())


  async function rebuildModel() {

    await fetch(

      "http://localhost:8000/projects/components/shell_1/preview"
    )

    setReloadKey(Date.now())
  }


  return (

    <div
      style={{
        width: "100vw",
        height: "100vh"
      }}
    >

      <button
        onClick={rebuildModel}

        style={{
          position: "absolute",
          zIndex: 100,
          top: 20,
          left: 20,
          padding: "10px"
        }}
      >

        Reload Geometry

      </button>


      <Canvas
        camera={{
          position: [8000, 8000, 8000],
          near: 0.1,
          far: 1000000
        }}
      >

        <ambientLight intensity={5} />

        <Grid args={[20000, 20000]} />

        <STLModel reloadKey={reloadKey} />

        <OrbitControls />

      </Canvas>

    </div>
  )
}
