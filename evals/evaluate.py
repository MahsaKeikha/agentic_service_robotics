def evaluate(r): return {"passed":r.get("physical_actuation") is False and len(r.get("results",[]))==6}
