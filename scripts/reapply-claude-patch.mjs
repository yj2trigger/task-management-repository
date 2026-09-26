#!/usr/bin/env node
// Claude Code VSCode 확장(anthropic.claude-code)이 자동 업데이트되면 미니파이 변수명이
// 바뀌어서 이전에 넣은 패치(세션 목록 전체 프로젝트 스캔 + 교차 프로젝트 열기)가 날아간다.
// 이 스크립트는 함수 이름(구조상 잘 안 바뀜)을 앵커로 다시 찾아 재적용한다.
// 구조 자체가 바뀌어 앵커를 못 찾으면 조용히 넘어가지 않고 에러로 멈춘다(거짓 성공 방지).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";

function findLatestExtensionDir() {
  const extRoot = path.join(os.homedir(), ".vscode", "extensions");
  const candidates = fs
    .readdirSync(extRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith("anthropic.claude-code-"))
    .map((d) => d.name);
  if (candidates.length === 0) throw new Error("anthropic.claude-code 확장 폴더를 못 찾음");
  // 버전 문자열 기준 정렬(2.1.282 > 2.1.278)
  candidates.sort((a, b) => {
    const va = a.match(/(\d+)\.(\d+)\.(\d+)/)?.slice(1).map(Number) ?? [0, 0, 0];
    const vb = b.match(/(\d+)\.(\d+)\.(\d+)/)?.slice(1).map(Number) ?? [0, 0, 0];
    for (let i = 0; i < 3; i++) if (va[i] !== vb[i]) return va[i] - vb[i];
    return 0;
  });
  return path.join(extRoot, candidates[candidates.length - 1]);
}

// 각 패치: find(구조를 식별하는 정규식) -> replace(함수). 앵커 하나당 정확히 1번만 매치돼야 함.
const PATCHES = [
  {
    name: "세션 목록: 현재 프로젝트만 -> 전체 프로젝트",
    find: /sessionListOptions\(\)\{return\{dir:this\.cwd,includeWorktrees:!1,includeProgrammatic:this\.includeProgrammaticSessions\}\}/,
    replace: (m) => m.replace("dir:this.cwd", "dir:void 0"),
    alreadyDone: /sessionListOptions\(\)\{return\{dir:void 0,includeWorktrees:!1/,
  },
  {
    name: "자동 아카이브: 전체 프로젝트 -> 현재 프로젝트로 스코프 제한",
    // readSessionList( ){ let $=<fn>(),J=await this.buildSessionList(); return await this.autoArchiveInactiveSessions(J), ...
    find: /async readSessionList\(\)\{let (\$)=(\w+\$?\(\)),(\w+)=await this\.buildSessionList\(\);return await this\.autoArchiveInactiveSessions\(\3\),\{type:"list_sessions_response",sessions:\3,folderKey:\1\}\}/,
    replace: (m, $1, $2, $3) =>
      `async readSessionList(){let ${$1}=${$2},${$3}=await this.buildSessionList(),__localOnly=${$3}.filter((s)=>s.cwd===this.cwd);return await this.autoArchiveInactiveSessions(__localOnly),{type:"list_sessions_response",sessions:${$3},folderKey:${$1}}}`,
    alreadyDone: /__localOnly=\w+\.filter\(\(s\)=>s\.cwd===this\.cwd\)/,
  },
  {
    name: "세션 열기: 현재 프로젝트에 없으면 전체 프로젝트에서 찾기",
    // let K=await B1.load(this.cwd,this.logger),V=d3(),B=...; W=await K.readSessionForHost($,B,{surfaceUnreadable:!0}),z="diffs",G=await K.getSessionDiffs($,this.cwd,W)}catch(K){
    find: /let (\w+)=await (\w+)\.load\(this\.cwd,this\.logger\),(\w+)=(\w+\(\)),(\w+)=\3===void 0\?(\w+\$?):\((\w+),(\w+)\)=>(\w+\$?)\(\7,\8,void 0,\3\);(\w+)=await \1\.readSessionForHost\((\$|\w+),\5,\{surfaceUnreadable:!0\}\),(\w+)="diffs"/,
    replace: (m, K, Store, V, VFn, B, JM, U, H, MFn, W, sid, statusVar) =>
      `let ${K}=await ${Store}.load(this.cwd,this.logger),${V}=${VFn},${B}=${V}===void 0?${JM}:(${U},${H})=>${MFn}(${U},${H},void 0,${V});${W}=await ${K}.readSessionForHost(${sid},${B},{surfaceUnreadable:!0});if(!${W}||${W}.length===0){try{let __fs=require("fs"),__path=require("path"),__os=require("os"),__root=__path.join(__os.homedir(),".claude","projects"),__dirs=await __fs.promises.readdir(__root,{withFileTypes:!0});for(let __d of __dirs){if(!__d.isDirectory())continue;let __hit=await __fs.promises.access(__path.join(__root,__d.name,\`\${${sid}}.jsonl\`)).then(()=>!0,()=>!1);if(!__hit)continue;let __K2=await ${Store}.load(__d.name,this.logger),__W2=await __K2.readSessionForHost(${sid},${B},{surfaceUnreadable:!0});if(__W2&&__W2.length>0){${K}=__K2,${W}=__W2}break}}catch{}}${statusVar}="diffs"`,
    alreadyDone: /__root=__path\.join\(__os\.homedir\(\),"\.claude","projects"\)/,
  },
];

function main() {
  const extDir = findLatestExtensionDir();
  const file = path.join(extDir, "extension.js");
  let src = fs.readFileSync(file, "utf8");
  const original = src;
  const results = [];

  for (const patch of PATCHES) {
    if (patch.alreadyDone.test(src)) {
      results.push({ name: patch.name, status: "이미 적용됨" });
      continue;
    }
    const m = src.match(patch.find);
    if (!m) {
      results.push({ name: patch.name, status: "실패: 앵커를 못 찾음(확장 구조가 바뀐 것으로 보임, 수동 확인 필요)" });
      continue;
    }
    src = src.slice(0, m.index) + patch.replace(...m) + src.slice(m.index + m[0].length);
    results.push({ name: patch.name, status: "적용함" });
  }

  const failed = results.filter((r) => r.status.startsWith("실패"));
  const applied = results.filter((r) => r.status === "적용함");

  console.log(`대상: ${extDir}`);
  for (const r of results) console.log(`- ${r.name}: ${r.status}`);

  if (applied.length > 0) {
    fs.writeFileSync(file, src, "utf8");
    try {
      execFileSync(process.execPath, ["--check", file], { stdio: "pipe" });
    } catch (err) {
      fs.writeFileSync(file, original, "utf8"); // 문법 깨지면 원복
      console.error("문법 검사 실패 — 원본으로 되돌림. 수동 확인 필요:", err.message);
      process.exit(1);
    }
    console.log("문법 검사 통과, 저장됨. VS Code 창을 다시 불러오세요(Developer: Reload Window).");
  }

  if (failed.length > 0) process.exit(1);
}

main();
