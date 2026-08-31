import { useEffect, useState } from 'react'

export default function Alerts(){
  const [alerts, setAlerts] = useState<any[]>([])

  useEffect(()=>{
    const token = localStorage.getItem('token')
    fetch('/api/alerts?unread_only=false', {headers: {'Authorization': `Bearer ${token}`}})
      .then(r=>r.json()).then(d=>setAlerts(d.rows || []))
  },[])

  const ack = async (id:number) =>{
    const token = localStorage.getItem('token')
    await fetch(`/api/alerts/${id}/ack`, {method:'POST', headers:{'Authorization': `Bearer ${token}`}})
    setAlerts(alerts.filter(a=>a.id!==id))
  }

  return (
    <div style={{padding:20}}>
      <h2>Alerts</h2>
      {alerts.map(a=> (
        <div key={a.id} style={{border:'1px solid #ddd', padding:8, margin:8}}>
          <div><strong>{a.alert_type}</strong> [{a.severity}]</div>
          <div>{a.message}</div>
          <div>{a.created_at}</div>
          {!a.read && <button onClick={()=>ack(a.id)}>Acknowledge</button>}
        </div>
      ))}
    </div>
  )
}
