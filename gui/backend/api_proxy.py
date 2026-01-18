def get_status(): return {"stage":"ANALYZE"}
def get_progress(): return {"percent":45}
def get_phases():
    return {"INIT":100,"ANALYZE":45,"PLAN":0,"DIFF":0,"APPLY":0}
def get_log():
    return {"lines":[
        "[INIT] Project loaded",
        "[ANALYZE] Reading files",
        "[ANALYZE] Found placeholders"
    ]}
