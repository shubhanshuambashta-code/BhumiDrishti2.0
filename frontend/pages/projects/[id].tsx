import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'

export default function ProjectDetail(){
  const router = useRouter()
  const { id } = router.query
  const [project, setProject] = useState<any>(null)
  const [explain, setExplain] = useState<any>(null)
  const [beforeAfter, setBeforeAfter] = useState<any>(null)

  useEffect(()=>{
    if (!id) return
    const token = localStorage.getItem('token')
    fetch(`/api/projects/${id}`, {headers:{'Authorization': `Bearer ${token}`}}).then(r=>r.json()).then(d=>setProject(d))
    fetch(`/api/projects/${id}/explain`, {headers:{'Authorization': `Bearer ${token}`}}).then(r=>r.json()).then(d=>setExplain(d))
  },[id])

  const runIntervention = async () =>{
    const token = localStorage.getItem('token')
    // example intervention: reduce pending approvals and compensation pending
    const adjustments = {pending_approvals: 0, compensation_pending_percentage: Math.max(0, (project.compensation_pending_percentage||0)-40), possession_percentage: Math.min(100, (project.possession_percentage||0)+30)}
    const res = await fetch(`/api/projects/${id}/intervene`, {method:'POST', headers:{'Authorization': `Bearer ${token}`,'Content-Type':'application/json'}, body: JSON.stringify(adjustments)})
    const data = await res.json()
    setBeforeAfter(data)
  }

  if (!project) return <div>Loading...</div>
  return (
    <div style={{padding:20}}>
      <h1>{project.project_name}</h1>
      <div>District: {project.district} | State: {project.state}</div>
      <div>Type: {project.project_type}</div>
      <h3>Risk & Prediction</h3>
      <button onClick={runIntervention}>Run Intervention Simulator (demo)</button>
      {beforeAfter && (
        <div>
          <h4>Before</h4>
          <pre>{JSON.stringify(beforeAfter.before, null, 2)}</pre>
          <h4>After</h4>
          <pre>{JSON.stringify(beforeAfter.after, null, 2)}</pre>
          <div>Delta score: {beforeAfter.delta_score}</div>
        </div>
      )}

      <h3>SHAP Explanation</h3>
      <pre>{JSON.stringify(explain, null, 2)}</pre>
    </div>
  )
}
