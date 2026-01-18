async function get(u){const r=await fetch(u);return r.ok?r.json():null}

async function sendIntent(intent, params = {}) {
    const payload = {
        command_id: crypto.randomUUID(),
        intent: intent,
        timestamp: new Date().toISOString(),
        params: params
    };
    const r = await fetch('/api/intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    return r.json();
}

async function refresh(){
    const s=await get('/api/status'),p=await get('/api/progress'),ph=await get('/api/phases'),l=await get('/api/log'),as=await get('/api/autonomy_status');
    
    if (as) {
        const badge = document.getElementById('sandboxBadge');
        const toggle = document.getElementById('sandbox_toggle');
        if (badge) badge.style.display = as.sandbox_mode ? 'inline' : 'none';
        if (toggle) toggle.checked = as.sandbox_mode;
        document.body.classList.toggle('sandbox-active', as.sandbox_mode);

        // Handle Verification Mode UI
        const isVerification = as.gui_mode === 'sandbox_advisory';
        document.body.classList.toggle('verification-mode', isVerification);

        const llmToggle = document.getElementById('llm_sandbox_toggle');
        if (llmToggle) llmToggle.checked = as.llm_sandbox_enabled;
        
        const advisoryContent = document.getElementById('llmAdvisoryContent');
        const contextData = document.getElementById('contextData');

        if (as.llm_sandbox_enabled) {
            get('/api/sandbox/analyze').then(data => {
                if (data && data.analysis) advisoryContent.textContent = data.analysis;
                if (data && data.context && contextData) {
                    contextData.textContent = JSON.stringify(data.context, null, 2);
                }
            });
        } else {
            if (advisoryContent) advisoryContent.textContent = 'LLM Sandbox Disabled';
            if (contextData) contextData.textContent = 'LLM Sandbox Disabled';
        }
    }

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
    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.onclick = () => {
            const taskText = document.getElementById('taskText')?.value || "";
            sendIntent('START_ANALYSIS', { task_text: taskText });
        };
    }

    const stopBtn = document.getElementById('stopBtn');
    if (stopBtn) stopBtn.onclick = () => sendIntent('STOP_EXECUTION');

    const modeSwitch = document.getElementById('autonomy_mode_switch');
    if (modeSwitch) {
        modeSwitch.onchange = (e) => {
            const newMode = e.target.value;
            if (confirm(`Switch to ${newMode} mode?`)) {
                sendIntent('SET_AUTONOMY_MODE', { mode: newMode });
            } else {
                // Revert selection if cancelled
                get('/api/autonomy_status').then(data => {
                    if (data) modeSwitch.value = data.gui_mode;
                });
            }
        };
        // Initial sync
        get('/api/autonomy_status').then(data => {
            if (data) modeSwitch.value = data.gui_mode || 'E2';
        });
    }
    
    const llmSandboxToggle = document.getElementById('llm_sandbox_toggle');
    if (llmSandboxToggle) {
        llmSandboxToggle.onchange = (e) => {
            const enabled = e.target.checked;
            if (enabled) {
                if (confirm("Enable LLM Sandbox (Advisory Mode)? This will send context to LLM for analysis.")) {
                    sendIntent('TOGGLE_LLM_SANDBOX', { enabled: true });
                } else {
                    e.target.checked = false;
                }
            } else {
                sendIntent('TOGGLE_LLM_SANDBOX', { enabled: false });
            }
        };
    }

    const sandboxToggle = document.getElementById('sandbox_toggle');
    if (sandboxToggle) {
        sandboxToggle.onchange = (e) => {
            const enabled = e.target.checked;
            if (enabled) {
                if (confirm("Sandbox mode enabled. Changes will not affect production.")) {
                    sendIntent('TOGGLE_SANDBOX', { enabled: true });
                } else {
                    e.target.checked = false;
                }
            } else {
                sendIntent('TOGGLE_SANDBOX', { enabled: false });
            }
        };
    }

    const resultBtns = document.querySelectorAll('.result .buttons button');
    resultBtns.forEach(btn => {
        if (btn.textContent.includes('Применить изменения')) {
            btn.onclick = () => {
                get('/api/autonomy_status').then(data => {
                    if (data && data.sandbox_mode) {
                        if (confirm("Apply sandbox results to production?")) {
                            sendIntent('PROMOTE_SANDBOX');
                        }
                    } else {
                        sendIntent('APPLY_DIFF');
                    }
                });
            };
        }
        if (btn.textContent.includes('Откатить')) btn.onclick = () => sendIntent('ROLLBACK');
        if (btn.textContent.includes('Посмотреть Diff')) btn.onclick = () => sendIntent('REQUEST_DIFF');
        if (btn.textContent.includes('Отчёт')) btn.onclick = () => sendIntent('REQUEST_PLAN');
    });
});

setInterval(refresh, 1000);
refresh();
