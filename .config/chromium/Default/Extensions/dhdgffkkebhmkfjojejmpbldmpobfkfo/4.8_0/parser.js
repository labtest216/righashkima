'use strict';Registry.require(["helper","compat","i18n"],function(){var h=Registry.get("helper"),p=Registry.get("compat"),t=Registry.get("i18n"),q=function(){this.uuid=null;this.observers=[];this.name=this.supportURL=this.updateURL=this.downloadURL=this.fileURL=this.icon64=this.icon=null;this.name_i18n={};this.description=this.homepage=this.namespace=this.version=null;this.description_i18n={};this.system=!1;this.enabled=!0;this.position=0;this.grant=[];this.requires=[];this.includes=[];this.matches=
[];this.excludes=[];this.resources=[];this.connects=[];this.blockers=[];this.lastModified=0;this.webRequest=this.version=null;this.sync={imported:!1};this.options={check_for_updates:!0,comment:null,compatopts_for_requires:!0,compat_wrappedjsobject:!1,compat_metadata:!1,compat_foreach:!1,compat_arrayleft:!1,compat_prototypes:!1,compat_uW_gmonkey:!1,compat_forvarin:!1,noframes:null,awareOfChrome:!1,run_at:null,override:{use_includes:[],orig_includes:[],merge_includes:!0,use_matches:[],orig_matches:[],
merge_matches:!0,use_excludes:[],orig_excludes:[],merge_excludes:!0,use_connects:[],merge_connects:!0,use_blockers:[],orig_run_at:null,orig_noframes:null}}},r={Script:q,processMetaHeader:function(a){var b={};a=a.replace(/\t/g,"    ");a=a.replace(/\r/g,"\n");a=a.replace(/\n\n+/g,"\n");a=a.replace(/[^|\n][ \t]+\/\//g,"//");var c,e;a.split("\n").forEach(function(a){c=a.replace(/^[\t\s]*\/\//gi,"").replace(/^[\t\s]*/gi,"").replace(/\s\s+/gi," ");h.each({"uso:hash":!1,version:!1},function(a,k){var f=new RegExp("^@"+
k+"[\\t\\s]","i"),d=a||k;-1!=c.search(f)&&(e=c.replace(f,"").replace(/[ \b\r\n]/gi,"").trim(),""!==e&&(b[d]=b[d]||e))})});return b},processHeader:function(a){var b=new q;a=a.replace(/\t/g,"    ");a=a.replace(/\r/g,"\n");a=a.replace(/\n\n+/g,"\n");a=a.replace(/[^|\n][ \t]+\/\//g,"//");var c,e,n,g;a.split("\n").forEach(function(a){n=a.replace(/^[\t\s]*\/\//gi,"").replace(/^[\t\s]*/gi,"");e=n.replace(/\s\s+/gi," ");g=!1;h.each({name:!1,description:!1},function(a,c){var m=a||c,f=null!==b[m],d=e.match(new RegExp("^@"+
c+"(\\[[a-zA-Z_\\-0-9]+\\]|:[a-zA-Z_\\-0-9]+|#[a-zA-Z_\\-0-9]+"+(f?"| [a-zA-Z_\\-0-9]+":"")+")?[\\t\\s]+(.*)$"));if(d&&3===d.length&&(g=d[2].replace(/[\r\n]/gi,"").trim(),void 0!==g&&""!==g))if(f){var h,m=m+"_i18n";d[1]&&(h=d[1].match("[a-zA-Z_\\-0-9]+"))&&h[0]&&(d=t.normalizeLocale(h[0]),b[m][d]=g)}else b[m]=g});h.each({version:!1,updateURL:!1,downloadURL:!1,supportURL:!1,homepage:!1,homepageURL:"homepage",website:"homepage",source:"homepage",uuid:!1},function(a,c){var d=new RegExp("^@"+c+"[\\t\\s]",
"i"),f=a||c;-1!=e.search(d)&&(g=e.replace(d,"").replace(/[ \b\r\n]/gi,"").trim(),""!==g&&(b[f]=b[f]||g))});h.each({webRequest:!1,icon:!1,iconURL:"icon",defaulticon:"icon",icon64:!1,iconURL64:"icon64"},function(a,c){var d=new RegExp("^@"+c+"[\\t\\s]","i"),f=a||c;-1!=e.search(d)&&(g=e.replace(d,"").replace(/[\b\r\n]/gi,"").trim(),""!==g&&(b[f]=b[f]||g))});h.each({namespace:!1,author:!1,copyright:!1},function(a,c){var e=new RegExp("^@"+c+"[\\t\\s]","i"),d=a||c;-1!=n.search(e)&&(g=n.replace(e,"").replace(/[\b\r\n]/gi,
"").trim(),""!==g&&(b[d]=b[d]||g))});h.each({"run-at":"run_at"},function(a,c){var d=new RegExp("^@"+c+"[\\t\\s]","i"),f=a||c;-1!=e.search(d)&&(g=e.replace(d,"").replace(/[\r\n]/gi,"").trim(),""!==g&&(b.options[f]=b.options[f]||g))});var f=function(a){return a.trim().replace(/ /gi,"%20").replace(/[\b\r\n]/gi,"")};h.each({include:"includes",match:"matches",exclude:"excludes",connect:"connects","connect-src":"connects",domain:"connects"},function(a,c){var d=new RegExp("^@"+c+"[\\t\\s]","i"),h=a||c;-1!=
e.search(d)&&(g=f(e.replace(d,"")).trim())&&b[h].push(g)});-1!=e.search(/^@require[\t\s]/)&&(g=f(e.replace(/^@require[\t\s]*/gi,"")).trim())&&b.requires.push({url:g,loaded:!1,textContent:""});if(-1!=e.search(/^@resource[\t\s]/)&&(g=e.replace(/^@resource[\t\s]*/gi,"").trim(),c=g.split(" "),2<=c.length)){a=c.shift();var d=f(c.join(" "));""!==a&&d&&b.resources.push({name:a,url:d,loaded:!1})}-1!=e.search(/^@grant[\t\s]/)&&(g=e.replace(/^@grant/gi,"").replace(/[\b\r\n]/gi,"").trim())&&b.grant.push(g);
h.each({noframes:!1,nocompat:"awareOfChrome"},function(a,c){var d=a||c;-1!=e.search(new RegExp("^@"+c+"[\\t\\s\\r\\n]?"))&&(b.options[d]=!0)})});b.version||(b.version="0.0");if(b.webRequest)try{b.webRequest=JSON.parse(b.webRequest)}catch(k){return console.warn("parser: unable to process webRequest header",b.webRequest),new q}return b},getHeaderTags:function(){return{start:"==UserScript==",stop:"==/UserScript=="}},getHeader:function(a){var b=h.getStringBetweenTags(a,"==UserScript==","==/UserScript==");
if(!b)return null;var c=a.search("==UserScript=="),e=a.search("<html>");a=a.search("<body>");return 0<e&&e<c||0<a&&a<c?null:b},createScriptFromSrc:function(a){a=(a||"").replace(/(\r\n|\n|\r)/gm,"\n");var b=r.getHeader(a);if(!b)return{};var c=r.processHeader(b);c.textContent=a;c.header=b;c.options.awareOfChrome||(c.options.compat_wrappedjsobject=a!=p.unWrappedJsObjectify(a),c.options.compat_metadata=a!=p.unMetaDataify(a),c.options.compat_prototypes=p.findPrototypes(a));-1!=a.search("unsafeWindow.gmonkey")&&
(c.options.compat_uW_gmonkey=!0);return c},versionCmp:function(){var a=function(a){a=a.split(".");return a.slice(0,3).concat([a.slice(3).join(".")]).concat([0,0,0,0]).slice(0,4).map(function(a){a=a.toString().match(/((?:\-?[0-9]+)?)([^0-9\-]*)((?:\-?[0-9]+)?)(.*)/);return[Number(a[1]),a[2],Number(a[3]),a[4]]}).reduce(function(a,b){return a.concat(b)})},b=function(c,e){for(var h=Array.isArray(c)?c:a(c),g=Array.isArray(e)?e:a(e),k=0;16>k;k++){var f=h[k],d=g[k];if(1===k%2){if(!f&&d)return b.eNEWER;if(f&&
!d)return b.eOLDER;for(var f=f.match(/\w/g)||[],d=d.match(/\w/g)||[],l=0;l<Math.min(f.length,d.length);l++){if(f[l].charCodeAt(0)>d[l].charCodeAt(0))return b.eNEWER;if(f[l].charCodeAt(0)<d[l].charCodeAt(0))return b.eOLDER}if(f.length>d.length)return b.eNEWER;if(f.length<d.length)return b.eOLDER}else{if(Number(f)>Number(d))return b.eNEWER;if(Number(f)<Number(d))return b.eOLDER}}return b.eEQUAL};b.__proto__.eERROR=-2;b.__proto__.eOLDER=-1;b.__proto__.eEQUAL=0;b.__proto__.eNEWER=1;return b}()};Registry.register("parser",
"5904",r)});
