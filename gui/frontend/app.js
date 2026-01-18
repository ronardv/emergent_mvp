async function get(u){const r=await fetch(u);return r.ok?r.json():null}
async function post(u){const r=await fetch(u,{method:'POST'});return r.json()}

async function refresh(){
    const s=await get('/api/status'),p=await get('/api/progress'),ph=await get('/api/phases'),l=await get('/api/log');
    const stageEl = document.getElementById('currentStage');
    if (stageEl) stageEl.textContent=s?.stage||'НЕТ ДАННЫХ';
    const progressEl = document.getElementById('progressBar');
    if (progressEl) progressEl.style.width=p?p.percent+'%':'0%';
    const list=document.getElementById('phases');
    if (list) {
        list.innerHTML='';
        if(ph){
            for(const k in ph){
                const li=document.createElement('li');
                li.textContent=k+' — '+ph[k]+'%';
                list.appendChild(li);
            }
        }else{
            list.innerHTML='<li>НЕТ ДАННЫХ</li>';
        }
    }
    const logEl = document.getElementById('logOutput');
    if (logEl) logEl.textContent=l?l.lines.join('\n'):'НЕТ ДАННЫХ';
}

document.addEventListener('DOMContentLoaded', () => {
    const btns = {
        'startBtn': '/api/start',
        'stopBtn': '/api/stop'
    };
    for (const id in btns) {
        const el = document.getElementById(id);
        if (el) el.onclick = () => post(btns[id]);
    }
    
    // Result section buttons by text content as they don't have IDs in index.html
    const resultBtns = document.querySelectorAll('.result .buttons button');
    resultBtns.forEach(btn => {
        if (btn.textContent.includes('Применить изменения')) btn.onclick = () => post('/api/apply');
        if (btn.textContent.includes('Откатить')) btn.onclick = () => post('/api/rollback');
    });
});

setInterval(refresh, 1000);
refresh();
