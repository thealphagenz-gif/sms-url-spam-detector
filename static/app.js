const smsInput=document.getElementById("sms-input");
smsInput.addEventListener("input",()=>document.getElementById("sms-count").textContent=`${smsInput.value.length} / 5000`);
document.querySelectorAll(".example-chip").forEach(b=>b.addEventListener("click",()=>{document.getElementById("url-input").value=b.dataset.url;document.getElementById("url-input").focus()}));
function esc(v){return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function render(box,d,kind){
 const risk=d.risk||"Low",cl=risk==="High"?"high":risk==="Medium"?"medium":"";
 const score=kind==="url"?d.risk_score:d.spam_probability;
 const label=kind==="url"?"URL pattern risk score":"Model-estimated spam probability";
 const items=(d.indicators&&d.indicators.length)?d.indicators.map(x=>`<li>${esc(x)}</li>`).join(""):"<li>No extra indicators found.</li>";
 box.innerHTML=`<div class="result-top"><div class="result-title">${esc(d.label)}</div><span class="risk-pill ${cl}">${esc(risk.toUpperCase())} RISK</span></div><div class="score-line"><span>${label}</span><b>${Number(score||0).toFixed(1)}%</b></div><div class="meter"><div class="meter-fill ${cl}" style="width:${Math.max(0,Math.min(100,Number(score||0)))}%"></div></div><ul class="result-list">${items}</ul>${kind==="url"?`<div class="result-note">Domain checked: ${esc(d.host||"Unknown")}</div>`:""}<div class="result-note">${esc(d.note||"")}</div>`;
 box.classList.remove("hidden");
}
async function run(button,endpoint,input,box,kind){
 const value=input.value.trim();if(!value){input.focus();box.innerHTML='<div class="result-title">Input required</div><div class="result-note">Please enter text before running analysis.</div>';box.classList.remove("hidden");return}
 button.disabled=true;const old=button.innerHTML;button.innerHTML="<span>Analyzing…</span><span>◌</span>";
 try{const r=await fetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(kind==="sms"?{message:value}:{url:value})});const d=await r.json();if(!r.ok)throw new Error(d.error||"Analysis failed.");render(box,d,kind)}
 catch(e){box.innerHTML=`<div class="result-title">Could not analyze</div><div class="result-note">${esc(e.message)} Make sure the Flask server is running.</div>`;box.classList.remove("hidden")}
 finally{button.disabled=false;button.innerHTML=old}
}
document.getElementById("sms-submit").addEventListener("click",function(){run(this,"/api/sms",smsInput,document.getElementById("sms-result"),"sms")});
document.getElementById("url-submit").addEventListener("click",function(){run(this,"/api/url",document.getElementById("url-input"),document.getElementById("url-result"),"url")});
smsInput.addEventListener("keydown",e=>{if((e.ctrlKey||e.metaKey)&&e.key==="Enter")document.getElementById("sms-submit").click()});
document.getElementById("url-input").addEventListener("keydown",e=>{if(e.key==="Enter")document.getElementById("url-submit").click()});
