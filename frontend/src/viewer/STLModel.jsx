import { useLoader } from "@react-three/fiber"

import { STLLoader } from "three-stdlib"


export default function STLModel({
  stlUrl,
  reloadKey
}) {

  const geometry = useLoader(
    STLLoader,

    `${stlUrl}?v=${reloadKey}`
  )

  geometry.center()

  return (

    <mesh geometry={geometry}>

      <meshNormalMaterial />

    </mesh>
  )
}
