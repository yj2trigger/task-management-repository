#!/usr/bin/env node
// applyPatchesToSource()가 실제 extension.js 구조를 목업한 문자열에도 세 패치를 다 찾아
// 적용하는지 확인. Claude Code 확장이 미니파이 변수명을 바꿀 때마다(2.1.283에서 z->W로
// 바뀌어 패치3 앵커가 깨졌던 사고, git log 6a2ace5) 회귀를 잡기 위한 것.
import assert from "node:assert/strict";
import { applyPatchesToSource } from "./reapply-claude-patch.mjs";

// 패치1 앵커: sessionListOptions()
const MOCK1 = `sessionListOptions(){return{dir:this.cwd,includeWorktrees:!1,includeProgrammatic:this.includeProgrammaticSessions}}`;

// 패치2 앵커: readSessionList()
const MOCK2 = `async readSessionList(){let $=XY$(),K9=await this.buildSessionList();return await this.autoArchiveInactiveSessions(K9),{type:"list_sessions_response",sessions:K9,folderKey:$}}`;

// 패치3 앵커: readSessionForHost 호출부. statusVar 이름을 바꿔가며 두 벌 만들어
// "미니파이 변수명이 바뀌어도 정규식이 잡는지"를 검증한다.
function mockPatch3(statusVarName) {
  return `let K1=await q1.load(this.cwd,this.logger),V1=JJ1(),B1=V1===void 0?xj$:(H1,U1)=>qA$(H1,U1,void 0,V1);z1=await K1.readSessionForHost($,B1,{surfaceUnreadable:!0}),${statusVarName}="diffs"`;
}

function demo() {
  // 1) 구버전 변수명(z)과 신버전 변수명(W) 둘 다 처음엔 "적용함"이어야 함
  for (const statusVar of ["z", "W"]) {
    const mockSrc = `${MOCK1}\n${MOCK2}\n${mockPatch3(statusVar)}`;
    const { src: patched, results } = applyPatchesToSource(mockSrc);
    assert.equal(results.length, 3, `패치 3개 결과 나와야 함 (statusVar=${statusVar})`);
    for (const r of results) {
      assert.equal(r.status, "적용함", `${r.name}: ${r.status} (statusVar=${statusVar})`);
    }
    // 문법상 깨지지 않았는지: 패치 후 문자열에 각 alreadyDone 앵커가 남아있어야 함
    assert.match(patched, /dir:void 0,includeWorktrees:!1/);
    assert.match(patched, /__localOnly=\w+\.filter\(\(s\)=>s\.cwd===this\.cwd\)/);
    assert.match(patched, /__root=__path\.join\(__os\.homedir\(\),"\.claude","projects"\)/);

    // 2) 같은 결과물에 다시 돌리면 셋 다 "이미 적용됨"이어야 함(멱등성)
    const { results: results2 } = applyPatchesToSource(patched);
    for (const r of results2) {
      assert.equal(r.status, "이미 적용됨", `재실행 시 ${r.name}: ${r.status} (statusVar=${statusVar})`);
    }
  }

  console.log("전부 통과: 패치3 회귀 없음(구버전/신버전 변수명 둘 다 매치), 멱등성 확인.");
}

demo();
