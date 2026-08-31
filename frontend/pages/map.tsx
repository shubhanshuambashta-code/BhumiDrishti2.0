import dynamic from 'next/dynamic'
import { useEffect, useRef } from 'react'

const Map = dynamic(() => import('maplibre-gl'), { ssr: false })

export default function MapPage(){
  const mapRef = useRef<any>(null)

  useEffect(()=>{
    let mapInstance: any
    async function init(){
      const maplibregl = (await import('maplibre-gl')).default
      mapInstance = new maplibregl.Map({
        container: 'map',
        style: 'https://demotiles.maplibre.org/style.json',
        center: [78, 23],
        zoom: 4
      })
      mapRef.current = mapInstance

      const res = await fetch('/api/map/projects')
      const data = await res.json()
      // add markers
      data.features.forEach((f:any)=>{
        const el = document.createElement('div')
        el.className = 'marker'
        el.style.width = '18px'
        el.style.height = '18px'
        el.style.background = '#b91c1c'
        el.style.borderRadius = '50%'
        const marker = new maplibregl.Marker(el).setLngLat(f.geometry.coordinates).setPopup(new maplibregl.Popup().setText(f.properties.project_name)).addTo(mapInstance)
      })
    }
    init()
    return ()=>{ if (mapInstance) mapInstance.remove() }
  },[])

  return (
    <div style={{height:'80vh'}}>
      <h2>Risk Map (Demo)</h2>
      <div id="map" style={{width:'100%', height:'100%'}}></div>
    </div>
  )
}
