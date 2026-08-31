import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Dashboard(){
  const [projects, setProjects] = useState<any[]>([])

  useEffect(()=>{
    const token = localStorage.getItem('token')
    fetch('/api/projects?limit=20', {headers: {'Authorization': `Bearer ${token}`}})
      .then(r=>r.json()).then(d=>setProjects(d.rows || []))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>BHUMIDRISHTI — Dashboard (Demo)</h1>
      <div>
        {projects.map(p=> (
          <div key={p.project_id} style={{border:'1px solid #ccc', padding:10, margin:8}}>
            <h3>{p.project_name}</h3>
            <div>District: {p.district} | Type: {p.project_type}</div>
            <div>Delayed: {p.delayed ? 'Yes' : 'No'}</div>
            <Link href={`/projects/${p.project_id}`}><a>Open</a></Link>
          </div>
        ))}
      </div>
    </div>
  )
}
