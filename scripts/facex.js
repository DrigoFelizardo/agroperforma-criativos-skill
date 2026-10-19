// node facex.js <project> a:b [a:b ...] -> mean face cx/cy in each range
const fs=require("fs");const L=JSON.parse(fs.readFileSync(process.argv[2]+"/media/faces.json"));
process.argv.slice(3).forEach(r=>{const [a,b]=r.split(":").map(Number);const v=L.filter(f=>f.t>=a+0.1&&f.t<b-0.05);const m=k=>(v.reduce((x,f)=>x+f[k],0)/v.length).toFixed(3);console.log(r,"cx",m("cx"),"cy",m("cy"),"n",v.length)});
