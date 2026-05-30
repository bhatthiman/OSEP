import { useEffect, useState } from "react"

import { Canvas } from "@react-three/fiber"

import {
  OrbitControls,
  Grid
} from "@react-three/drei"

import STLModel from "./STLModel"


export default function Viewer({
  stlUrl
}) {

  const [reloadKey, setReloadKey] =
    useState(Date.now())


  // -----------------------------------
  // Reload model whenever URL changes
  // -----------------------------------

  useEffect(() => {

    setReloadKey(Date.now())

  }, [stlUrl])


  return (

    <div
      style={{
        width: "100vw",
        height: "100vh"
      }}
    >

      <Canvas
        camera={{
          position: [8000, 8000, 8000],
          near: 0.1,
          far: 1000000
        }}
      >

        <ambientLight intensity={5} />

        <Grid args={[20000, 20000]} />

        <STLModel
          stlUrl={stlUrl}
          reloadKey={reloadKey}
        />

        <OrbitControls />

      </Canvas>

    </div>
  )
}
