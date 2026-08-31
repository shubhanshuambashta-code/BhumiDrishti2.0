import { useEffect, useState } from 'react'

export default function TasksInbox(){
  const [tasks, setTasks] = useState<any[]>([])

  useEffect(()=>{ load() },[])

  const load = async () =>{
    const token = localStorage.getItem('token')
    const res = await fetch('/api/tasks/inbox', {headers:{'Authorization': `Bearer ${token}`}})
    const data = await res.json()
    setTasks(data.tasks||[])
  }

  const claim = async (id:number) =>{
    const token = localStorage.getItem('token')
    await fetch(`/api/tasks/${id}/claim`, {method:'POST', headers:{'Authorization': `Bearer ${token}`}})
    load()
  }

  return (
    <div style={{padding:20}}>
      <h2>Task Inbox</h2>
      {tasks.map(t=> (
        <div key={t.id} style={{border:'1px solid #ddd', padding:8, margin:8}}>
          <div><strong>{t.title}</strong> [{t.status}]</div>
          <div>Project: {t.project_id}</div>
          <div>Assigned: {t.assigned_role || t.assigned_user}</div>
          {t.assigned_user===null && ( <button onClick={()=>claim(t.id)}>Claim task</button> )}
        </div>
      ))}
    </div>
  )
}
