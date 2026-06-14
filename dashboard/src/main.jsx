import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  AlertTriangle,
  BarChart3,
  BookOpen,
  CheckCircle2,
  Clipboard,
  Code2,
  Database,
  Download,
  ExternalLink,
  FileJson,
  FileText,
  Globe2,
  Layers3,
  Loader2,
  Monitor,
  RefreshCw,
  Save,
  Search,
  Settings2,
  SlidersHorizontal,
  Sparkles,
  Table2,
  XCircle
} from "lucide-react";
import "./styles.css";

const VIEWS = [
  { id: "recommendations", label: "Recommendations", icon: SlidersHorizontal },
  { id: "pages", label: "Radisson Pages", icon: Globe2 },
  { id: "sources", label: "Sources", icon: BookOpen },
  { id: "metadata", label: "Metadata", icon: Table2 },
  { id: "copy", label: "Copy Bank", icon: Clipboard },
  { id: "exports", label: "Exports", icon: Download }
];

const DEFAULT_FILTERS = {
  query: "",
  minScore: "0",
  surface: "all",
  evidence: "all",
  page: "all"
};

const api = {
  get: async (path) => request(path),
  post: async (path, payload = {}) => request(path, { method: "POST", body: JSON.stringify(payload) }),
  put: async (path, payload = {}) => request(path, { method: "PUT", body: JSON.stringify(payload) })
};

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  const data = await response.json();
  if (!response.ok) {
    const error = new Error(data.error || `Request failed with ${response.status}`);
    error.payload = data;
    throw error;
  }
  return data;
}

function App() {
  const [view, setView] = useState("recommendations");
  const [runs, setRuns] = useState([]);
  const [selectedRunId, setSelectedRunId] = usePersistentState("geo:selectedRunId", "");
  const [filters, setFilters] = usePersistentObject("geo:filters", DEFAULT_FILTERS);
  const [data, setData] = useState(null);
  const [selectedRecommendationId, setSelectedRecommendationId] = useState("");
  const [selectedPageUrl, setSelectedPageUrl] = useState("");
  const [selectedSourceId, setSelectedSourceId] = useState("");
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    loadRuns();
  }, []);

  useEffect(() => {
    if (!selectedRunId && runs.length) {
      setSelectedRunId(runs[runs.length - 1].run_id);
    }
  }, [runs, selectedRunId, setSelectedRunId]);

  useEffect(() => {
    if (selectedRunId) {
      loadDashboard(selectedRunId);
    }
  }, [selectedRunId]);

  async function loadRuns() {
    setError("");
    try {
      const payload = await api.get("/api/dashboard/runs");
      setRuns(payload.runs || []);
    } catch (err) {
      setError(err.message);
    }
  }

  async function loadDashboard(runId) {
    setBusy("load");
    setError("");
    try {
      const payload = await api.get(`/api/dashboard/data?run_id=${encodeURIComponent(runId)}`);
      setData(payload);
      const firstRecommendation = payload.recommendations?.[0]?.proposal_id || "";
      const stillExists = payload.recommendations?.some((item) => item.proposal_id === selectedRecommendationId);
      if (!selectedRecommendationId || !stillExists) setSelectedRecommendationId(firstRecommendation);
      if (!selectedPageUrl && payload.radisson_pages?.length) setSelectedPageUrl(payload.radisson_pages[0].canonical_url);
      if (!selectedSourceId && payload.sources?.length) setSelectedSourceId(payload.sources[0].source_id);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  async function importRun() {
    if (!selectedRunId) return;
    setBusy("import");
    setError("");
    try {
      const payload = await api.post("/api/dashboard/import", { run_id: selectedRunId });
      setData(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  async function capturePage(pageUrl) {
    if (!selectedRunId || !pageUrl) return;
    setBusy(`capture:${pageUrl}`);
    setError("");
    try {
      const payload = await api.post("/api/dashboard/capture", { run_id: selectedRunId, url: pageUrl });
      setData(payload.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  async function saveOverride(proposalId, override) {
    if (!selectedRunId || !proposalId) return;
    setBusy(`override:${proposalId}`);
    setError("");
    try {
      const payload = await api.put("/api/dashboard/overrides", {
        run_id: selectedRunId,
        proposal_id: proposalId,
        override
      });
      setData(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy("");
    }
  }

  const recommendations = useMemo(() => filterRecommendations(data?.recommendations || [], filters), [data, filters]);
  const selectedRecommendation = useMemo(
    () => (data?.recommendations || []).find((item) => item.proposal_id === selectedRecommendationId) || recommendations[0] || null,
    [data, selectedRecommendationId, recommendations]
  );
  const lookups = useMemo(() => buildLookups(data), [data]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">RG</div>
          <div>
            <h1>GEOptimizer</h1>
            <p>Radisson audit dashboard</p>
          </div>
        </div>
        <nav className="nav-list">
          {VIEWS.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={view === item.id ? "nav-item active" : "nav-item"}
                onClick={() => setView(item.id)}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
        <div className="sidebar-footer">
          <span className={data?.run?.validation_errors?.length ? "status-dot danger" : "status-dot live"} />
          <span>{data?.run?.run_id || "No run loaded"}</span>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <p className="eyeline">Internal audit tool</p>
            <h2>Recommendation-first GEOptimizer research</h2>
          </div>
          <div className="topbar-actions">
            <label className="run-select">
              Run
              <select value={selectedRunId} onChange={(event) => setSelectedRunId(event.target.value)}>
                {runs.map((run) => (
                  <option key={run.run_id} value={run.run_id}>
                    {run.run_id} · {run.date}
                  </option>
                ))}
              </select>
            </label>
            <button className="secondary-button" onClick={importRun} disabled={!selectedRunId || busy === "import"}>
              {busy === "import" ? <Loader2 className="spin" size={16} /> : <Database size={16} />}
              <span>Re-import</span>
            </button>
            <button className="icon-button" onClick={() => loadDashboard(selectedRunId)} disabled={!selectedRunId || busy === "load"} title="Refresh">
              <RefreshCw size={18} />
            </button>
          </div>
        </header>

        {error && (
          <div className="alert">
            <AlertTriangle size={18} />
            <span>{error}</span>
          </div>
        )}

        {!data ? (
          <div className="loading-panel">
            <Loader2 className="spin" size={24} />
            <span>Loading GEOptimizer run data</span>
          </div>
        ) : (
          <>
            <SummaryBar data={data} />
            {view === "recommendations" && (
              <RecommendationsView
                data={data}
                recommendations={recommendations}
                selectedRecommendation={selectedRecommendation}
                selectedRecommendationId={selectedRecommendationId}
                filters={filters}
                setFilters={setFilters}
                setSelectedRecommendationId={setSelectedRecommendationId}
                lookups={lookups}
                saveOverride={saveOverride}
                busy={busy}
              />
            )}
            {view === "pages" && (
              <PagesView
                data={data}
                selectedPageUrl={selectedPageUrl}
                setSelectedPageUrl={setSelectedPageUrl}
                setSelectedRecommendationId={setSelectedRecommendationId}
                setView={setView}
                capturePage={capturePage}
                busy={busy}
                lookups={lookups}
              />
            )}
            {view === "sources" && (
              <SourcesView
                data={data}
                selectedSourceId={selectedSourceId}
                setSelectedSourceId={setSelectedSourceId}
                setSelectedRecommendationId={setSelectedRecommendationId}
                setView={setView}
              />
            )}
            {view === "metadata" && <MetadataView data={data} lookups={lookups} />}
            {view === "copy" && <CopyBankView data={data} saveOverride={saveOverride} busy={busy} />}
            {view === "exports" && <ExportsView runId={selectedRunId} />}
          </>
        )}
      </main>
    </div>
  );
}

function SummaryBar({ data }) {
  const validationCount = data.run?.validation_errors?.length || 0;
  return (
    <section className="summary-grid">
      <Metric label="Recommendations" value={data.summary?.recommendations || 0} />
      <Metric label="Ready Evidence" value={data.summary?.implementation_ready || 0} />
      <Metric label="Sources" value={data.summary?.sources || 0} />
      <Metric label="Selector Warnings" value={data.summary?.selector_warnings || 0} danger={Boolean(data.summary?.selector_warnings)} />
      <Metric label="Validation Errors" value={validationCount} danger={Boolean(validationCount)} />
    </section>
  );
}

function RecommendationsView({
  data,
  recommendations,
  selectedRecommendation,
  selectedRecommendationId,
  filters,
  setFilters,
  setSelectedRecommendationId,
  lookups,
  saveOverride,
  busy
}) {
  return (
    <section className="detail-layout">
      <div className="main-column">
        <FilterBar data={data} filters={filters} setFilters={setFilters} />
        <div className="panel table-panel">
          <PanelHeader icon={SlidersHorizontal} label="Ranked by combined score" title="Recommendations" />
          <div className="recommendation-list">
            {recommendations.map((rec) => (
              <button
                key={rec.proposal_id}
                className={selectedRecommendationId === rec.proposal_id ? "recommendation-row active" : "recommendation-row"}
                onClick={() => setSelectedRecommendationId(rec.proposal_id)}
              >
                <span className="score">{rec.combined_score}</span>
                <span className="row-main">
                  <strong>{rec.proposal_id} · {rec.title}</strong>
                  <small>{rec.page_refs?.join(" · ") || "Portfolio-wide"}</small>
                </span>
                <span className="row-meta">
                  <Tag>{rec.surface}</Tag>
                  <EvidenceTag tier={rec.evidence_tier} />
                  <SelectorTag status={rec.selector_status} />
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
      <RecommendationDetail recommendation={selectedRecommendation} data={data} lookups={lookups} saveOverride={saveOverride} busy={busy} />
    </section>
  );
}

function FilterBar({ data, filters, setFilters }) {
  const surfaces = unique((data.recommendations || []).map((rec) => rec.surface));
  const pages = unique((data.recommendations || []).flatMap((rec) => rec.page_refs || []));
  function update(key, value) {
    setFilters({ ...filters, [key]: value });
  }
  return (
    <div className="panel filter-panel">
      <label className="search-box">
        <Search size={17} />
        <input value={filters.query} onChange={(event) => update("query", event.target.value)} placeholder="Search recommendations, pages, evidence, copy" />
      </label>
      <label>
        Min score
        <select value={filters.minScore} onChange={(event) => update("minScore", event.target.value)}>
          <option value="0">All</option>
          <option value="60">60+</option>
          <option value="75">75+</option>
          <option value="90">90+</option>
        </select>
      </label>
      <label>
        Surface
        <select value={filters.surface} onChange={(event) => update("surface", event.target.value)}>
          <option value="all">All surfaces</option>
          {surfaces.map((surface) => <option key={surface} value={surface}>{surface}</option>)}
        </select>
      </label>
      <label>
        Evidence
        <select value={filters.evidence} onChange={(event) => update("evidence", event.target.value)}>
          <option value="all">All evidence</option>
          <option value="Implementation-ready">Implementation-ready</option>
          <option value="Medium evidence">Medium evidence</option>
          <option value="Validation error">Validation error</option>
        </select>
      </label>
      <label>
        Page
        <select value={filters.page} onChange={(event) => update("page", event.target.value)}>
          <option value="all">All pages</option>
          {pages.map((page) => <option key={page} value={page}>{shortUrl(page)}</option>)}
        </select>
      </label>
    </div>
  );
}

function RecommendationDetail({ recommendation, data, lookups, saveOverride, busy }) {
  if (!recommendation) {
    return (
      <aside className="detail-column pinned">
        <div className="panel"><p className="empty-text">Select a recommendation.</p></div>
      </aside>
    );
  }
  const sources = (recommendation.evidence_source_ids || []).map((id) => lookups.sources.get(id)).filter(Boolean);
  const copyBlocks = (data.copy_blocks || []).filter((block) => block.proposal_id === recommendation.proposal_id);
  return (
    <aside className="detail-column pinned">
      <div className="panel detail-card">
        <PanelHeader icon={Sparkles} label="Recommendation detail" title={`${recommendation.proposal_id} · ${recommendation.combined_score}`} />
        <h3>{recommendation.title}</h3>
        <div className="tag-row">
          <Tag>{recommendation.surface}</Tag>
          <EvidenceTag tier={recommendation.evidence_tier} />
          <SelectorTag status={recommendation.selector_status} />
        </div>
        <dl className="definition-list">
          <div><dt>Page</dt><dd>{recommendation.page_refs?.join(", ") || "Portfolio-wide"}</dd></div>
          <div><dt>Section</dt><dd>{recommendation.section_label || "Unspecified"}</dd></div>
          <div><dt>Selector</dt><dd>{recommendation.inferred_dom_selector || recommendation.selector_status}</dd></div>
        </dl>
      </div>

      <div className="panel">
        <PanelHeader icon={FileText} label="Before / after" title="Change Context" />
        <CompareBlock before={recommendation.before_after?.before || recommendation.current_state} after={recommendation.before_after?.after || recommendation.proposed_change} />
      </div>

      <OverrideEditor recommendation={recommendation} copyBlocks={copyBlocks} saveOverride={saveOverride} busy={busy} />

      <div className="panel">
        <PanelHeader icon={BookOpen} label={`${sources.length} linked`} title="Evidence Sources" />
        <div className="source-stack">
          {sources.map((source) => (
            <details key={source.source_id} className="source-detail">
              <summary>
                <strong>{source.headline || source.title_or_url}</strong>
                {source.url && <ExternalLink size={14} />}
              </summary>
              {source.url && <a href={source.url} target="_blank" rel="noreferrer">{source.url}</a>}
              <p>{source.ai_assessment_prose || "No assessment text parsed."}</p>
              <pre>{source.full_excerpt}</pre>
            </details>
          ))}
        </div>
      </div>

      <DiagramPanel title="Evidence Chain" diagram={recommendation.diagram} />
    </aside>
  );
}

function OverrideEditor({ recommendation, copyBlocks, saveOverride, busy }) {
  const existing = recommendation.team_override || {};
  const [selectorOverride, setSelectorOverride] = useState(existing.selector_override || "");
  const [notes, setNotes] = useState(existing.notes || "");
  const [priority, setPriority] = useState(existing.adjusted_priority_components || recommendation.priority_components || {});
  const [adjustedCopy, setAdjustedCopy] = useState(existing.adjusted_copy || {});

  useEffect(() => {
    setSelectorOverride(existing.selector_override || "");
    setNotes(existing.notes || "");
    setPriority(existing.adjusted_priority_components || recommendation.priority_components || {});
    setAdjustedCopy(existing.adjusted_copy || {});
  }, [recommendation.proposal_id]);

  function updatePriority(key, value) {
    setPriority({ ...priority, [key]: Number(value) });
  }

  function save() {
    saveOverride(recommendation.proposal_id, {
      selector_override: selectorOverride,
      notes,
      adjusted_priority_components: priority,
      adjusted_copy: adjustedCopy
    });
  }

  return (
    <div className="panel">
      <PanelHeader icon={Settings2} label="Stored separately" title="Team Adjustments" />
      <label className="field">
        Selector override
        <input value={selectorOverride} onChange={(event) => setSelectorOverride(event.target.value)} placeholder="e.g. main h1 or meta:title" />
      </label>
      <div className="priority-grid">
        {[
          ["business_impact", "Impact"],
          ["geo_relevance", "GEO"],
          ["evidence_strength", "Evidence"],
          ["ease_of_implementation", "Ease"]
        ].map(([key, label]) => (
          <label key={key}>
            {label}
            <input type="number" min="0" max="5" value={priority[key] ?? 0} onChange={(event) => updatePriority(key, event.target.value)} />
          </label>
        ))}
      </div>
      {copyBlocks.slice(0, 2).map((block) => (
        <label className="field" key={block.copy_block_id}>
          Adjusted copy · {block.copy_label}
          <textarea
            value={adjustedCopy[block.copy_block_id] || ""}
            onChange={(event) => setAdjustedCopy({ ...adjustedCopy, [block.copy_block_id]: event.target.value })}
            placeholder={block.export_value}
          />
        </label>
      ))}
      <label className="field">
        Internal notes
        <textarea value={notes} onChange={(event) => setNotes(event.target.value)} placeholder="Implementation note or decision context" />
      </label>
      <button className="primary-button wide" onClick={save} disabled={busy === `override:${recommendation.proposal_id}`}>
        {busy === `override:${recommendation.proposal_id}` ? <Loader2 className="spin" size={16} /> : <Save size={16} />}
        <span>Save overrides</span>
      </button>
    </div>
  );
}

function PagesView({ data, selectedPageUrl, setSelectedPageUrl, setSelectedRecommendationId, setView, capturePage, busy, lookups }) {
  const selectedPage = data.radisson_pages.find((page) => page.canonical_url === selectedPageUrl) || data.radisson_pages[0];
  const recs = (selectedPage?.recommendations || []).map((id) => lookups.recommendations.get(id)).filter(Boolean);
  return (
    <section className="page-workspace">
      <div className="panel page-list-panel">
        <PanelHeader icon={Globe2} label="Registry and audit pages" title="Radisson Pages" />
        <div className="page-list">
          {data.radisson_pages.map((page) => (
            <button key={page.canonical_url} className={page.canonical_url === selectedPage?.canonical_url ? "page-row active" : "page-row"} onClick={() => setSelectedPageUrl(page.canonical_url)}>
              <strong>{page.page_label}</strong>
              <small>{shortUrl(page.canonical_url)}</small>
              <span>{page.recommendations?.length || 0} recs</span>
            </button>
          ))}
        </div>
      </div>
      <div className="main-column">
        <div className="panel browser-panel">
          <div className="page-header">
            <div>
              <p className="eyeline">Live browser workspace</p>
              <h3>{selectedPage?.page_label}</h3>
              <a href={selectedPage?.source_url || selectedPage?.canonical_url} target="_blank" rel="noreferrer">
                {selectedPage?.source_url || selectedPage?.canonical_url} <ExternalLink size={14} />
              </a>
            </div>
            <button className="primary-button" onClick={() => capturePage(selectedPage?.source_url || selectedPage?.canonical_url)} disabled={busy === `capture:${selectedPage?.canonical_url}`}>
              {busy.startsWith("capture:") ? <Loader2 className="spin" size={16} /> : <Monitor size={16} />}
              <span>Capture page</span>
            </button>
          </div>
          <CapturePreview capture={selectedPage?.live_capture_refs} />
        </div>

        <div className="two-column">
          <div className="panel">
            <PanelHeader icon={Table2} label="Imported vs live" title="Metadata Snapshot" />
            <KeyValueTable rows={[
              ["Imported title", selectedPage?.metadata_snapshot?.title],
              ["Imported meta", selectedPage?.metadata_snapshot?.meta_description],
              ["Fetch status", selectedPage?.metadata_snapshot?.fetch_status],
              ["Live title", selectedPage?.live_capture_refs?.metadata?.title],
              ["Live description", selectedPage?.live_capture_refs?.metadata?.description],
              ["Capture status", selectedPage?.live_capture_refs?.status]
            ]} />
          </div>
          <div className="panel">
            <PanelHeader icon={Layers3} label="Selector candidates" title="DOM Targets" />
            <div className="selector-list">
              {(selectedPage?.live_capture_refs?.selector_candidates || []).slice(0, 12).map((item, index) => (
                <div key={`${item.selector}-${index}`} className="selector-item">
                  <strong>{item.label}</strong>
                  <code>{item.selector}</code>
                </div>
              ))}
              {!selectedPage?.live_capture_refs?.selector_candidates?.length && <p className="empty-text">Capture this page to inspect DOM selectors.</p>}
            </div>
          </div>
        </div>

        <div className="panel">
          <PanelHeader icon={SlidersHorizontal} label={`${recs.length} linked`} title="Recommendations For This Page" />
          <div className="compact-card-grid">
            {recs.map((rec) => (
              <button key={rec.proposal_id} className="compact-card" onClick={() => {
                setSelectedRecommendationId(rec.proposal_id);
                setView("recommendations");
              }}>
                <span className="score">{rec.combined_score}</span>
                <strong>{rec.proposal_id} · {rec.title}</strong>
                <small>{rec.section_label} · {rec.selector_status}</small>
              </button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function CapturePreview({ capture }) {
  if (!capture || capture.status === "not_captured") {
    return (
      <div className="capture-empty">
        <Monitor size={28} />
        <span>No browser capture stored for this run yet.</span>
      </div>
    );
  }
  return (
    <div className="capture-preview">
      {capture.screenshot_url ? (
        <img src={capture.screenshot_url} alt="Captured Radisson page" />
      ) : (
        <div className="capture-empty"><AlertTriangle size={24} /><span>No screenshot available.</span></div>
      )}
      <div className="capture-meta">
        <Tag>{capture.capture_method || "capture"}</Tag>
        <Tag>{capture.status || "unknown"}</Tag>
        {capture.playwright_error && <span className="warning-text">Playwright fallback: {capture.playwright_error}</span>}
      </div>
    </div>
  );
}

function SourcesView({ data, selectedSourceId, setSelectedSourceId, setSelectedRecommendationId, setView }) {
  const [sourceQuery, setSourceQuery] = useState("");
  const [findingGroup, setFindingGroup] = useState("all");
  const [scoreFilter, setScoreFilter] = useState("all");
  const sourceGroups = useMemo(
    () => [...new Set(data.sources.map((source) => source.finding_group).filter(Boolean))].sort(),
    [data.sources]
  );
  const filteredSources = useMemo(() => {
    const query = sourceQuery.trim().toLowerCase();
    return data.sources.filter((source) => {
      const haystack = [
        source.source_id,
        source.title_or_url,
        source.url,
        source.headline,
        source.finding_group,
        source.ai_assessment_prose,
        source.full_excerpt,
        ...(source.related_criteria || []),
        ...(source.related_gaps || []),
        ...(source.related_recommendations || [])
      ].join(" ").toLowerCase();
      if (query && !haystack.includes(query)) return false;
      if (findingGroup !== "all" && source.finding_group !== findingGroup) return false;
      if (scoreFilter === "ai" && !source.scorecard?.mentions_ai_engine) return false;
      if (scoreFilter === "schema" && !source.scorecard?.mentions_schema) return false;
      if (scoreFilter === "traveler" && !source.scorecard?.mentions_traveler) return false;
      if (scoreFilter === "linked" && !(source.related_recommendations || []).length) return false;
      return true;
    });
  }, [data.sources, sourceQuery, findingGroup, scoreFilter]);
  const selected = filteredSources.find((source) => source.source_id === selectedSourceId)
    || filteredSources[0]
    || data.sources.find((source) => source.source_id === selectedSourceId)
    || data.sources[0];
  return (
    <section className="detail-layout">
      <div className="main-column source-browser">
        <div className="panel source-hero">
          <PanelHeader icon={BookOpen} label={`${filteredSources.length} of ${data.sources.length} visible`} title="Source Library" />
          <div className="source-toolbar">
            <label className="search-box source-search">
              <Search size={16} />
              <input value={sourceQuery} onChange={(event) => setSourceQuery(event.target.value)} placeholder="Search sources, excerpts, criteria, recommendations" />
            </label>
            <label>
              Finding group
              <select value={findingGroup} onChange={(event) => setFindingGroup(event.target.value)}>
                <option value="all">All groups</option>
                {sourceGroups.map((group) => <option key={group} value={group}>{group}</option>)}
              </select>
            </label>
            <label>
              Signal
              <select value={scoreFilter} onChange={(event) => setScoreFilter(event.target.value)}>
                <option value="all">All signals</option>
                <option value="ai">Mentions AI engine</option>
                <option value="schema">Mentions schema</option>
                <option value="traveler">Mentions traveler</option>
                <option value="linked">Linked recommendations</option>
              </select>
            </label>
          </div>
        </div>
        <div className="source-card-grid" aria-label="Source cards">
          {filteredSources.map((source, index) => (
            <SourceCard
              key={source.source_id}
              source={source}
              index={index}
              selected={source.source_id === selected?.source_id}
              onSelect={() => setSelectedSourceId(source.source_id)}
            />
          ))}
        </div>
        {!filteredSources.length && (
          <div className="panel empty-card">
            <BookOpen size={24} />
            <strong>No sources match these filters.</strong>
            <span>Clear search or switch signal filters to review the full source library.</span>
          </div>
        )}
      </div>
      <aside className="detail-column pinned source-detail-panel" role="dialog" aria-modal="false" aria-labelledby="source-detail-title">
        <div className="panel">
          <PanelHeader icon={BookOpen} label="Full excerpt" title={selected?.finding_group || "Source"} />
          <h3 id="source-detail-title" className="source-detail-title">{sourceTitle(selected)}</h3>
          {selected?.url && <a className="external-link" href={selected.url} target="_blank" rel="noreferrer">{selected.url} <ExternalLink size={14} /></a>}
          <p className="assessment-text">{selected?.ai_assessment_prose}</p>
          <Scorecard scorecard={selected?.scorecard} />
          <div className="source-relations">
            <Tag>{(selected?.related_criteria || []).length} criteria</Tag>
            <Tag>{(selected?.related_gaps || []).length} gaps</Tag>
            <Tag>{(selected?.related_recommendations || []).length} recommendations</Tag>
          </div>
          <details className="excerpt-box" open>
            <summary>{selected?.headline || "Excerpt"}</summary>
            <pre>{selected?.full_excerpt}</pre>
          </details>
        </div>
        <div className="panel">
          <PanelHeader icon={SlidersHorizontal} label="Traceability" title="Linked Recommendations" />
          <div className="compact-card-grid">
            {(selected?.related_recommendations || []).map((id) => (
              <button key={id} className="compact-card" onClick={() => {
                setSelectedRecommendationId(id);
                setView("recommendations");
              }}>
                {id}
              </button>
            ))}
          </div>
        </div>
        <DiagramPanel title="Source Graph Slice" diagram={sourceGraphSlice(data, selected?.source_id)} />
      </aside>
    </section>
  );
}

function SourceCard({ source, index, selected, onSelect }) {
  const hasImage = Boolean(source.headerImage);
  return (
    <article className={selected ? "source-card selected" : "source-card"}>
      <button
        type="button"
        className="source-card-button"
        onClick={onSelect}
        aria-label={`Open source details: ${sourceTitle(source)}`}
        aria-pressed={selected}
      >
        <div className="source-card-media" style={sourceFallbackStyle(source, index)}>
          {hasImage ? (
            <img src={source.headerImage} alt="" loading="lazy" />
          ) : (
            <>
              <span className="source-domain-mark">{sourceDomain(source)}</span>
              <span className="source-media-label">{source.finding_group || "Source"}</span>
            </>
          )}
        </div>
        <div className="source-card-body">
          <div className="source-card-title-row">
            <strong>{sourceTitle(source)}</strong>
            {source.url && <ExternalLink size={15} aria-hidden="true" />}
          </div>
          <p>{sourceSubheader(source)}</p>
          <div className="source-card-tags">
            <Tag>{source.scorecard?.source_count ?? 0} refs</Tag>
            {source.scorecard?.mentions_ai_engine && <Tag ok>AI engine</Tag>}
            {source.scorecard?.mentions_schema && <Tag>Schema</Tag>}
            {source.scorecard?.mentions_traveler && <Tag>Traveler</Tag>}
            {(source.related_recommendations || []).length > 0 && <Tag>{source.related_recommendations.length} props</Tag>}
          </div>
        </div>
      </button>
    </article>
  );
}

function MetadataView({ data, lookups }) {
  const [groupBy, setGroupBy] = useState("page");
  const rows = data.metadata_changes || [];
  const groups = groupRows(rows, groupBy === "page" ? "page" : "field_name");
  return (
    <section className="main-column">
      <div className="panel view-toolbar">
        <PanelHeader icon={Table2} label={`${rows.length} changes`} title="Metadata Recommendations" />
        <label>
          Group by
          <select value={groupBy} onChange={(event) => setGroupBy(event.target.value)}>
            <option value="page">Page</option>
            <option value="field">Metadata field</option>
          </select>
        </label>
      </div>
      {Object.entries(groups).map(([group, items]) => (
        <div className="panel" key={group}>
          <PanelHeader icon={FileText} label={`${items.length} records`} title={group || "Unassigned"} />
          <div className="metadata-grid">
            {items.map((item) => (
              <div className="metadata-card" key={item.metadata_change_id}>
                <div className="metadata-card-head">
                  <strong>{item.field_name}</strong>
                  {item.warning ? <Tag danger>{item.warning}</Tag> : <Tag>Current</Tag>}
                </div>
                <CompareBlock before={item.current_value} after={item.proposed_value} />
                <button className="secondary-button" onClick={() => copyText(item.proposed_value)}>
                  <Clipboard size={15} />
                  <span>Copy proposed value</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}

function CopyBankView({ data, saveOverride, busy }) {
  const recommendations = buildLookups(data).recommendations;
  const byPage = groupRows(data.copy_blocks || [], "target_page");
  return (
    <section className="main-column">
      {Object.entries(byPage).map(([page, blocks]) => (
        <div className="panel" key={page || "unassigned"}>
          <PanelHeader icon={Clipboard} label={`${blocks.length} blocks`} title={page || "Portfolio-wide"} />
          <div className="copy-grid">
            {blocks.map((block) => (
              <CopyBlockCard
                key={block.copy_block_id}
                block={block}
                recommendation={recommendations.get(block.proposal_id)}
                saveOverride={saveOverride}
                busy={busy}
              />
            ))}
          </div>
        </div>
      ))}
    </section>
  );
}

function CopyBlockCard({ block, recommendation, saveOverride, busy }) {
  const [adjusted, setAdjusted] = useState(block.adjusted_text || "");
  useEffect(() => setAdjusted(block.adjusted_text || ""), [block.copy_block_id, block.adjusted_text]);
  function save() {
    const existing = recommendation?.team_override?.adjusted_copy || {};
    saveOverride(block.proposal_id, {
      ...(recommendation?.team_override || {}),
      adjusted_copy: { ...existing, [block.copy_block_id]: adjusted }
    });
  }
  return (
    <div className="copy-card">
      <div className="copy-card-head">
        <div>
          <strong>{block.copy_label}</strong>
          <small>{block.proposal_id} · {block.format_type}</small>
        </div>
        <button className="icon-button" title="Copy export value" onClick={() => copyText(block.export_value)}>
          <Clipboard size={16} />
        </button>
      </div>
      <div className="copy-compare">
        <div>
          <span>Original / GEOptimizer</span>
          <pre>{block.original_text || block.export_value}</pre>
        </div>
        <div>
          <span>Adjusted / export</span>
          <textarea value={adjusted} onChange={(event) => setAdjusted(event.target.value)} placeholder={block.export_value} />
        </div>
      </div>
      <button className="secondary-button" onClick={save} disabled={busy === `override:${block.proposal_id}`}>
        <Save size={15} />
        <span>Save adjusted copy</span>
      </button>
    </div>
  );
}

function ExportsView({ runId }) {
  const [exportType, setExportType] = useState("clipboard");
  const [content, setContent] = useState("");
  const [busy, setBusy] = useState("");
  async function loadExport(type = exportType) {
    setBusy(type);
    try {
      const payload = await api.get(`/api/dashboard/export?run_id=${encodeURIComponent(runId)}&type=${encodeURIComponent(type)}`);
      setContent(payload.content || "");
      setExportType(type);
    } finally {
      setBusy("");
    }
  }
  useEffect(() => {
    if (runId) loadExport("clipboard");
  }, [runId]);
  return (
    <section className="main-column">
      <div className="panel export-toolbar">
        <PanelHeader icon={Download} label="Handoff formats" title="Exports" />
        <div className="button-row">
          {[
            ["clipboard", Clipboard, "Clipboard bundle"],
            ["csv", Table2, "CSV"],
            ["json", FileJson, "JSON"],
            ["audit", FileText, "Full audit"]
          ].map(([type, Icon, label]) => (
            <button key={type} className={exportType === type ? "secondary-button selected" : "secondary-button"} onClick={() => loadExport(type)} disabled={busy === type}>
              {busy === type ? <Loader2 className="spin" size={15} /> : <Icon size={15} />}
              <span>{label}</span>
            </button>
          ))}
          <button className="primary-button" onClick={() => copyText(content)}>
            <Clipboard size={15} />
            <span>Copy current export</span>
          </button>
        </div>
      </div>
      <div className="panel">
        <pre className="export-preview">{content}</pre>
      </div>
    </section>
  );
}

function CompareBlock({ before, after }) {
  return (
    <div className="compare-grid">
      <div>
        <span>Before / current</span>
        <pre>{before || "Not parsed from source artifacts."}</pre>
      </div>
      <div>
        <span>After / proposed</span>
        <pre>{after || "Missing proposed copy."}</pre>
      </div>
    </div>
  );
}

function DiagramPanel({ title, diagram }) {
  const nodes = diagram?.nodes || [];
  const edges = diagram?.edges || [];
  return (
    <div className="panel">
      <PanelHeader icon={Layers3} label={`${nodes.length} nodes · ${edges.length} edges`} title={title} />
      <div className="diagram-box">
        {edges.slice(0, 16).map((edge, index) => (
          <div key={`${edge.from}-${edge.to}-${index}`} className="diagram-edge">
            <code>{edge.from}</code>
            <span>{edge.label || "links"}</span>
            <code>{edge.to}</code>
          </div>
        ))}
        {!edges.length && <p className="empty-text">No diagram edges parsed.</p>}
      </div>
    </div>
  );
}

function Scorecard({ scorecard }) {
  if (!scorecard) return null;
  return (
    <div className="scorecard">
      {Object.entries(scorecard).map(([key, value]) => (
        <div key={key}>
          <span>{labelize(key)}</span>
          <strong>{typeof value === "boolean" ? (value ? "Yes" : "No") : value}</strong>
        </div>
      ))}
    </div>
  );
}

function KeyValueTable({ rows }) {
  return (
    <div className="kv-table">
      {rows.map(([label, value]) => (
        <React.Fragment key={label}>
          <strong>{label}</strong>
          <span>{value || "Not available"}</span>
        </React.Fragment>
      ))}
    </div>
  );
}

function Metric({ label, value, danger = false }) {
  return (
    <div className={danger ? "metric danger" : "metric"}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function PanelHeader({ icon: Icon, label, title }) {
  return (
    <div className="panel-header">
      <Icon size={18} />
      <div>
        <span>{label}</span>
        <h3>{title}</h3>
      </div>
    </div>
  );
}

function Tag({ children, danger = false, warn = false, ok = false }) {
  const className = danger ? "tag danger" : warn ? "tag warn" : ok ? "tag ok" : "tag";
  return <span className={className}>{children}</span>;
}

function EvidenceTag({ tier }) {
  const danger = tier === "Validation error";
  return <span className={danger ? "tag danger" : tier === "Medium evidence" ? "tag warn" : "tag ok"}>{tier}</span>;
}

function SelectorTag({ status }) {
  const warning = String(status || "").toLowerCase().includes("warning");
  return <span className={warning ? "tag warn" : "tag"}>{status || "No selector"}</span>;
}

function buildLookups(data) {
  return {
    recommendations: new Map((data?.recommendations || []).map((item) => [item.proposal_id, item])),
    sources: new Map((data?.sources || []).map((item) => [item.source_id, item])),
    pages: new Map((data?.radisson_pages || []).map((item) => [item.canonical_url, item]))
  };
}

function filterRecommendations(recommendations, filters) {
  const query = filters.query.toLowerCase().trim();
  return recommendations.filter((rec) => {
    if (Number(rec.combined_score || 0) < Number(filters.minScore || 0)) return false;
    if (filters.surface !== "all" && rec.surface !== filters.surface) return false;
    if (filters.evidence !== "all" && rec.evidence_tier !== filters.evidence) return false;
    if (filters.page !== "all" && !(rec.page_refs || []).includes(filters.page)) return false;
    if (!query) return true;
    const haystack = [
      rec.proposal_id,
      rec.title,
      rec.surface,
      rec.section_label,
      rec.proposed_change,
      rec.current_state,
      ...(rec.page_refs || []),
      ...(rec.evidence_source_ids || [])
    ].join(" ").toLowerCase();
    return haystack.includes(query);
  });
}

function groupRows(rows, key) {
  return rows.reduce((acc, row) => {
    const group = row[key] || "Unassigned";
    acc[group] = acc[group] || [];
    acc[group].push(row);
    return acc;
  }, {});
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function sourceGraphSlice(data, sourceId) {
  if (!sourceId) return { nodes: [], edges: [] };
  const edges = (data.source_diagrams?.source_graph?.edges || []).filter((edge) => edge.from === sourceId || edge.to === sourceId);
  return { nodes: unique(edges.flatMap((edge) => [edge.from, edge.to])), edges };
}

function sourceTitle(source) {
  if (!source) return "Source";
  return source.title || source.title_or_url || source.url || source.headline || source.source_id || "Source";
}

function sourceSubheader(source) {
  if (!source) return "No summary parsed.";
  return source.subheader || source.headline || source.finding_group || source.url || "Source detail available.";
}

function sourceDomain(source) {
  const value = source?.url || source?.title_or_url || "";
  try {
    const parsed = new URL(value);
    return parsed.hostname.replace(/^www\./, "").split(".")[0].slice(0, 2).toUpperCase() || "SR";
  } catch {
    return String(source?.finding_group || source?.source_id || "SR").slice(0, 2).toUpperCase();
  }
}

function sourceFallbackStyle(source, index) {
  const palettes = [
    ["#dfeaf5", "#f8fbfd", "#1d5f9f"],
    ["#e4efe8", "#f8fbf9", "#287a4d"],
    ["#f3eadc", "#fffaf1", "#9b6400"],
    ["#eadfe6", "#fbf8fb", "#7a3f61"],
    ["#e2e7ea", "#fbfcfd", "#4d5c68"]
  ];
  const key = Array.from(String(source?.source_id || source?.finding_group || index)).reduce((total, char) => total + char.charCodeAt(0), 0);
  const palette = palettes[key % palettes.length];
  return {
    "--source-media-bg": palette[0],
    "--source-media-soft": palette[1],
    "--source-media-ink": palette[2]
  };
}

function labelize(value) {
  return String(value).replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

function shortUrl(value) {
  return String(value || "").replace(/^https?:\/\/(www\.)?/, "").replace(/\/$/, "");
}

function copyText(value) {
  navigator.clipboard.writeText(value || "");
}

function usePersistentState(key, defaultValue) {
  const [value, setValue] = useState(() => window.localStorage.getItem(key) || defaultValue);
  useEffect(() => {
    window.localStorage.setItem(key, value);
  }, [key, value]);
  return [value, setValue];
}

function usePersistentObject(key, defaultValue) {
  const [value, setValue] = useState(() => {
    try {
      return JSON.parse(window.localStorage.getItem(key)) || defaultValue;
    } catch {
      return defaultValue;
    }
  });
  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  return [value, setValue];
}

const rootElement = document.getElementById("root");
const root = window.__radissonDashboardRoot || createRoot(rootElement);
window.__radissonDashboardRoot = root;
root.render(<App />);
