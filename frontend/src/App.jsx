import React, { useEffect, useState } from 'react'
import { api, login, logout, token } from './api'

export default function App() {
  const [user, setUser] = useState(null), [page, setPage] = useState('dashboard')
  const [error, setError] = useState(''), [busy, setBusy] = useState(false)
  async function refreshUser() { if (token()) { try { setUser(await api('/auth/me/')) } catch { logout(); setUser(null) } } }
  useEffect(() => { refreshUser() }, [])
  async function handleLogin(e) {
    e.preventDefault(); setError(''); setBusy(true)
    const fd = new FormData(e.currentTarget)
    try { setUser(await login(fd.get('username'), fd.get('password'))) } catch (err) { setError(err.message) } finally { setBusy(false) }
  }
  async function handleRegister(e) {
    e.preventDefault(); setError(''); setBusy(true)
    const fd = new FormData(e.currentTarget)
    try {
      await api('/auth/register/', { method: 'POST', body: JSON.stringify(Object.fromEntries(fd)) })
      setError('Registration successful. Please log in.')
    } catch (err) { setError(err.message) } finally { setBusy(false) }
  }
  if (!user) return <main className="auth">
    <section className="hero"><span className="mark">UEH</span><h1>Ubuntu Enterprise Hub</h1><p>Connecting Eastern Cape businesses to support and opportunity.</p></section>
    <section className="panel"><h2>Sign in</h2><form onSubmit={handleLogin}><input name="username" placeholder="Username" required/><input name="password" type="password" placeholder="Password" required/><button disabled={busy}>Sign in</button></form>
    <details><summary>Create an MSME client account</summary><form onSubmit={handleRegister}>
      <input name="username" placeholder="Username" minLength="3" required/><input name="email" type="email" placeholder="Email" required/>
      <input name="password" type="password" placeholder="Password (10+ characters)" minLength="10" required/>
      <input name="first_name" placeholder="First name"/><input name="last_name" placeholder="Last name"/>
      <input name="business_name" placeholder="Business name"/><input name="phone" placeholder="Phone"/>
      <button disabled={busy}>Register</button></form></details>{error && <p className="error">{error}</p>}</section>
  </main>
  return <div className="layout"><aside><div className="brand">UEH <small>Enterprise Hub</small></div><p className="welcome">Hello, {user.first_name || user.username}</p>
    {['dashboard','requests','opportunities','applications'].map(x => <button className={page===x?'nav active':'nav'} onClick={()=>setPage(x)} key={x}>{x[0].toUpperCase()+x.slice(1)}</button>)}
    <button className="nav" onClick={()=>{logout();setUser(null)}}>Sign out</button></aside>
    <main className="content"><header><div><p className="eyebrow">UBUNTU ENTERPRISE HUB</p><h1>{page[0].toUpperCase()+page.slice(1)}</h1></div><span className="role">{user.role}</span></header>
      {error && <p className="error">{error}</p>}
      {page==='dashboard' && <Dashboard />}
      {page==='requests' && <Requests user={user}/>}
      {page==='opportunities' && <Opportunities user={user}/>}
      {page==='applications' && <Applications user={user}/>}
    </main>
  </div>
}

function Dashboard() {
  const [data,setData]=useState(null), [err,setErr]=useState('')
  useEffect(()=>{api('/dashboard/').then(setData).catch(e=>setErr(e.message))},[])
  if(err)return <p className="error">{err}</p>; if(!data)return <p>Loading dashboard…</p>
  return <><div className="stats">{[['Open requests',data.open_requests],['In progress',data.in_progress_requests],['Resolved',data.resolved_requests],['Applications',data.total_applications ?? data.my_applications ?? 0]].map(([k,v])=><article className="stat" key={k}><p>{k}</p><strong>{v}</strong></article>)}</div>
    {data.applications_per_opportunity && <section className="panel"><h2>Applications per opportunity</h2>{data.applications_per_opportunity.map(x=><p key={x.id}>{x.title} <b>{x.total}</b></p>)}</section>}</>
}
function Requests({user}) {
  const [items,setItems]=useState([]),[err,setErr]=useState('')
  async function load(){try{setItems(await api('/requests/'))}catch(e){setErr(e.message)}}
  useEffect(()=>{load()},[])
  async function create(e){e.preventDefault();const fd=new FormData(e.currentTarget);try{await api('/requests/',{method:'POST',body:JSON.stringify(Object.fromEntries(fd))});e.currentTarget.reset();load()}catch(e){setErr(e.message)}}
  async function update(id,patch){try{await api(`/requests/${id}/`,{method:'PATCH',body:JSON.stringify(patch)});load()}catch(e){setErr(e.message)}}
  return <><section className="panel"><h2>Log a support request</h2><form className="form-grid" onSubmit={create}><select name="category"><option value="FUNDING">Funding support</option><option value="BUSINESS">Business advice</option><option value="COMPLIANCE">Compliance</option><option value="MARKETING">Marketing</option><option value="OTHER">Other</option></select><select name="urgency"><option>LOW</option><option selected value="MEDIUM">MEDIUM</option><option>HIGH</option></select><textarea name="description" minLength="10" placeholder="Describe the support you need (at least 10 characters)" required/><button>Submit request</button></form></section>
  <section className="panel"><h2>Request tracking</h2>{err&&<p className="error">{err}</p>}{items.map(x=><article className="item" key={x.id}><div><b>#{x.id} · {x.category}</b><p>{x.description}</p><small>Urgency: {x.urgency} · Agent: {x.assigned_agent_name || 'Not assigned'}</small></div><div><span className="status">{x.status.replace('_',' ')}</span>{user.role!=='CLIENT' && <select value={x.status} onChange={e=>update(x.id,{status:e.target.value})}><option value="OPEN">Open</option><option value="IN_PROGRESS">In Progress</option><option value="RESOLVED">Resolved</option></select>}</div></article>)}</section></>
}
function Opportunities({user}) {
  const [items,setItems]=useState([]),[err,setErr]=useState('')
  async function load(){try{setItems(await api('/opportunities/'))}catch(e){setErr(e.message)}}
  useEffect(()=>{load()},[])
  async function post(e){e.preventDefault();const fd=new FormData(e.currentTarget);const data=Object.fromEntries(fd);data.is_published=true;try{await api('/opportunities/',{method:'POST',body:JSON.stringify(data)});e.currentTarget.reset();load()}catch(e){setErr(e.message)}}
  async function apply(id){const motivation=prompt('Explain why your business is suitable (at least 20 characters):');if(!motivation)return;try{await api(`/opportunities/${id}/apply/`,{method:'POST',body:JSON.stringify({motivation})});alert('Application submitted.')}catch(e){setErr(e.message)}}
  return <><section className="panel"><h2>Available opportunities</h2>{err&&<p className="error">{err}</p>}{items.map(x=><article className="item" key={x.id}><div><span className="tag">{x.opportunity_type}</span><h3>{x.title}</h3><p>{x.description}</p><small>Closing date: {x.closing_date || 'Not specified'}</small></div>{user.role==='CLIENT'&&<button onClick={()=>apply(x.id)}>Apply</button>}</article>)}</section>
  {(user.role==='ADMIN'||user.is_staff)&&<section className="panel"><h2>Post an opportunity</h2><form onSubmit={post}><input name="title" placeholder="Title" required/><select name="opportunity_type"><option>FUNDING</option><option>TENDER</option><option>TRAINING</option></select><textarea name="description" minLength="20" placeholder="Description (20+ characters)" required/><textarea name="eligibility" placeholder="Eligibility criteria"/><input name="closing_date" type="date"/><button>Publish</button></form></section>}</>
}
function Applications({user}) {
  const [items,setItems]=useState([]),[err,setErr]=useState('')
  async function load(){try{setItems(await api('/applications/'))}catch(e){setErr(e.message)}}
  useEffect(()=>{load()},[])
  async function review(id,status){try{await api(`/applications/${id}/`,{method:'PATCH',body:JSON.stringify({status})});load()}catch(e){setErr(e.message)}}
  return <section className="panel"><h2>{user.role==='CLIENT'?'My applications':'Review applications'}</h2>{err&&<p className="error">{err}</p>}{items.map(x=><article className="item" key={x.id}><div><b>{x.opportunity_title}</b><p>{x.motivation}</p><small>Applicant: {x.applicant_name} · {x.status}</small></div>{user.role==='ADMIN'&&<div><button onClick={()=>review(x.id,'UNDER_REVIEW')}>Review</button><button onClick={()=>review(x.id,'APPROVED')}>Approve</button><button className="secondary" onClick={()=>review(x.id,'DECLINED')}>Decline</button></div>}</article>)}</section>
}
