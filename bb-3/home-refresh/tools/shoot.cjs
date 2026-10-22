const {chromium}=require(process.env.HOME+'/.npm/_npx/9833c18b2d85bc59/node_modules/playwright');
(async()=>{const b=await chromium.launch({channel:'chrome'});
for(const [url,w,h,out,full] of JSON.parse(process.argv[2])){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(url);await p.waitForTimeout(1200);await p.screenshot({path:out,fullPage:!!full});await p.close();}
await b.close();})();
