import { useEffect, useState } from 'react'

export default function Audit(){
  const [logs, setLogs] = useState<any[]>([])

  useEffect(()=>{
    const token = localStorage.getItem('token')
    fetch('/api/audit-logs?limit=50', {headers: {'Authorization': `Bearer ${token}`}})
      .then(r=>{
        if (r.status===403) { setLogs([]); return {} }
        return r.json()
      }).then(d=>setLogs(d.rows || []))
  },[])

  return (
    <div style={{padding:20}}>
      <h2>Audit Logs (Admin)</h2>
      {logs.length===0 && <div>No audit logs or insufficient permissions</div>}
      {logs.map(l=> (
        <div key={l.id} style={{border:'1px solid #eee', padding:8, margin:8}}>
          <div><strong>{l.action}</strong> by {l.username} on {l.timestamp}</div>
          <div>Project: {l.project_id}</div>
          <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify({old: l.old_value, new: l.new_value}, null, 2)}</pre>
        </div>
      ))}
    </div>
  )
}
