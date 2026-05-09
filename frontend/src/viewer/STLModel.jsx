import { useLoader } from "@react-three/fiber"

import { STLLoader } from "three-stdlib"


export default function STLModel({
  reloadKey
}) {

  const geometry = useLoader(
    STLLoader,

    `http://localhost:8000/outputs/shell_1.stl?v=${reloadKey}`
  )

  geometry.center()

  return (

    <mesh geometry={geometry}>

      <meshNormalMaterial />

    </mesh>
  )
}
