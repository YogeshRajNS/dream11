"""
Dream 11 Team Generator — Streamlit version
Faithful conversion of the original HTML/JS single-page app.
Same 6-step wizard, same selection/uniqueness logic, same dark theme.

Run with:  streamlit run dream11_app.py
"""

import random
import streamlit as st

# ───────────────────────── CONSTANTS ─────────────────────────
ROLES = ['WK', 'BAT', 'ALL', 'BOWL']
SIZES = [11, 12, 13, 14, 15]
TOTAL_STEPS = 6
MAX_ATTEMPTS = 2000

ROLE_COLORS = {
    'WK':   '#a78bfa',
    'BAT':  '#34d399',
    'ALL':  '#fbbf24',
    'BOWL': '#f87171',
}

# ───────────────────────── PAGE CONFIG ─────────────────────────
st.set_page_config(page_title="Dream 11 Generator", page_icon="🏏", layout="centered")

# ───────────────────────── CSS (theme) ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;500;600;700&family=Orbitron:wght@400;700;900&display=swap');

:root {
  --bg: #0a0e1a;
  --surface: #111827;
  --surface2: #1a2236;
  --border: #1e3a5f;
  --accent: #00d4ff;
  --accent2: #ff6b35;
  --gold: #ffd700;
  --green: #00e676;
  --text: #e8f4fd;
  --muted: #7a9ab8;
  --wk: #a78bfa;
  --bat: #34d399;
  --all: #fbbf24;
  --bowl: #f87171;
}

.stApp {
  background-color: var(--bg);
  background-image:
    radial-gradient(ellipse at 20% 20%, rgba(0,212,255,0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 80%, rgba(255,107,53,0.06) 0%, transparent 50%);
}

html, body, [class*="css"]  {
  font-family: 'Rajdhani', sans-serif;
  color: var(--text);
}

h1, h2, h3 { font-family: 'Bebas Neue', sans-serif !important; letter-spacing: 3px; }

.d11-header { text-align:center; padding: 10px 0 6px; }
.d11-header h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(2.2rem, 6vw, 4rem);
  letter-spacing: 6px;
  background: linear-gradient(135deg, var(--accent), var(--gold), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}
.d11-header p { color: var(--muted); letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; font-size: 0.9rem;}
.d11-header::after {
  content: '';
  display: block;
  width: 200px; height: 2px;
  background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
  margin: 14px auto 0;
}

.d11-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 26px 26px 10px 26px; margin-bottom: 20px;
  position: relative;
}
.d11-card.team-a { border-top: 3px solid var(--accent); }
.d11-card.team-b { border-top: 3px solid var(--accent2); }
.d11-card.gold-top { border-top: 3px solid var(--gold); }

.d11-badge {
  display:inline-block; padding:2px 10px; border-radius:4px;
  font-family:'Orbitron', sans-serif; font-size:0.6rem; font-weight:700; letter-spacing:2px;
  margin-right: 8px;
}
.badge-a { background: rgba(0,212,255,0.15); color: var(--accent); border: 1px solid var(--accent); }
.badge-b { background: rgba(255,107,53,0.15); color: var(--accent2); border: 1px solid var(--accent2); }

.d11-steplabel {
  font-family:'Orbitron', sans-serif; font-size:0.62rem; color: var(--muted);
  letter-spacing:2px; text-transform:uppercase; margin-bottom: 10px;
}

.d11-info {
  background: rgba(0,212,255,0.06); border: 1px solid rgba(0,212,255,0.2);
  border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; color: var(--muted);
  margin-bottom: 16px;
}
.d11-info strong { color: var(--accent); }

/* progress dots */
.d11-progress { display:flex; justify-content:center; gap:6px; margin: 10px 0 24px; flex-wrap: wrap; }
.d11-dot {
  width:30px; height:30px; border-radius:50%; border:2px solid var(--border);
  display:flex; align-items:center; justify-content:center;
  font-family:'Orbitron', sans-serif; font-size:0.6rem; font-weight:700; color: var(--muted);
}
.d11-dot.active { border-color: var(--accent); color: var(--accent); box-shadow: 0 0 10px rgba(0,212,255,0.4); }
.d11-dot.done { background: var(--accent); border-color: var(--accent); color: var(--bg); }
.d11-line { width:20px; height:2px; background: var(--border); align-self:center; }
.d11-line.done { background: var(--accent); }

/* role badge pill */
.role-pill {
  display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; letter-spacing:1px;
}

.captain-badge { background:linear-gradient(135deg,var(--gold),#ff8c00); color:var(--bg); padding:2px 8px; border-radius:4px; font-size:0.62rem; font-weight:700; letter-spacing:1px; margin-left:7px; }
.vc-badge { background:rgba(192,192,192,0.25); color:#e8e8e8; padding:2px 8px; border-radius:4px; font-size:0.62rem; font-weight:700; letter-spacing:1px; margin-left:6px; }

.d11-result-name { font-family:'Bebas Neue', sans-serif; font-size:1.25rem; letter-spacing:3px; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid var(--border); }
.d11-result-name.a { color: var(--accent); }
.d11-result-name.b { color: var(--accent2); }

.d11-player-row { display:flex; align-items:center; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(30,58,95,0.5); font-size:0.92rem; font-weight:600; }

.d11-chip { padding:3px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; letter-spacing:1px; margin-right:6px; display:inline-block; margin-bottom:4px;}

.d11-diff-tag { display:inline-block; background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.3); color: var(--accent); padding:2px 8px; border-radius:4px; margin:2px; font-size:0.75rem; }

.batting-flag {
  display:inline-block; font-size:0.6rem; letter-spacing:1.5px;
  background:rgba(0,230,118,0.15); color: var(--green);
  padding:3px 8px; border-radius:4px; font-weight:700; margin-left: 8px;
}

div.stButton > button {
  border-radius: 10px !important;
  font-family: 'Orbitron', sans-serif !important;
  letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ───────────────────────── SESSION STATE ─────────────────────────
def init_state():
    defaults = {
        'step': 1,
        'sizeA': None,
        'sizeB': None,
        'numTeams': None,
        'batFirst': None,
        'playersA': [],
        'playersB': [],
        'generatedTeams': [],
        'err': {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def go_to(step):
    st.session_state.step = step
    st.rerun()

def set_err(key, msg):
    st.session_state.err[key] = msg

def clear_err(key):
    st.session_state.err.pop(key, None)

# ───────────────────────── HEADER ─────────────────────────
st.markdown("""
<div class="d11-header">
  <h1>DREAM 11 GENERATOR</h1>
  <p>Fantasy Cricket Team Builder</p>
</div>
""", unsafe_allow_html=True)

# ───────────────────────── PROGRESS BAR ─────────────────────────
def render_progress():
    current = st.session_state.step
    html = '<div class="d11-progress">'
    for i in range(1, TOTAL_STEPS + 1):
        cls = 'd11-dot'
        if i < current:
            cls += ' done'
        elif i == current:
            cls += ' active'
        html += f'<div class="{cls}">{i}</div>'
        if i < TOTAL_STEPS:
            line_cls = 'd11-line done' if i < current else 'd11-line'
            html += f'<div class="{line_cls}"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

render_progress()

# ───────────────────────── HELPERS ─────────────────────────
def shuffle(items):
    a = list(items)
    random.shuffle(a)
    return a

def team_key(players):
    return '|'.join(sorted(p['name'] for p in players))

def select_from_pool(pool, count):
    picked = []
    for role in ROLES:
        candidates = [p for p in pool if p['role'] == role]
        if not candidates:
            return None
        picked.append(random.choice(candidates))
    picked_ids = {id(p) for p in picked}
    remaining = shuffle([p for p in pool if id(p) not in picked_ids])
    combined = picked + remaining[:count - 4]
    return shuffle(combined)

def diff_count(team_a, team_b):
    names_a = {p['name'] for p in team_a}
    return sum(1 for p in team_b if p['name'] not in names_a)

def validate_players(players):
    if any((not p['name']) or (not p['role']) for p in players):
        return False
    return all(any(p['role'] == r for p in players) for r in ROLES)

def generate_all_teams():
    bat_first = st.session_state.batFirst
    bat_pool = st.session_state.playersA if bat_first == 'A' else st.session_state.playersB
    bowl_pool = st.session_state.playersB if bat_first == 'A' else st.session_state.playersA
    n = st.session_state.numTeams

    teams = []
    keys = set()

    for _t in range(n):
        found = False
        for _attempt in range(MAX_ATTEMPTS):
            sel1 = select_from_pool(bat_pool, 6)
            sel2 = select_from_pool(bowl_pool, 5)
            if sel1 is None or sel2 is None:
                break
            combined = sel1 + sel2
            key = team_key(combined)

            valid = key not in keys
            if valid:
                for prev in teams:
                    if diff_count(prev['combined'], combined) < 2:
                        valid = False
                        break
            if valid:
                shuffled_all = shuffle(combined)
                teams.append({
                    'sel1': sel1,
                    'sel2': sel2,
                    'combined': combined,
                    'captain': shuffled_all[0],
                    'vc': shuffled_all[1],
                })
                keys.add(key)
                found = True
                break
        if not found:
            st.warning(
                f"Could only generate {len(teams)} unique team(s) with at least 2 player "
                f"differences given your squad size. Try larger squads or fewer teams."
            )
            break

    st.session_state.generatedTeams = teams

# ═══════════════════════════════════════════════════════════════
# STEP 1 — Team A Squad Size
# ═══════════════════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="d11-steplabel">Step 1 of 6 — Squad Size</div>', unsafe_allow_html=True)
    st.markdown('<div class="d11-card team-a">', unsafe_allow_html=True)
    st.markdown('<span class="d11-badge badge-a">TEAM A</span> **How many players?**', unsafe_allow_html=True)
    st.caption("Select squad size for Team A")

    cols = st.columns(len(SIZES))
    for i, n in enumerate(SIZES):
        selected = st.session_state.sizeA == n
        if cols[i].button(f"{n}\nPlayers", key=f"sizeA_{n}", type="primary" if selected else "secondary", use_container_width=True):
            st.session_state.sizeA = n
            st.rerun()

    if st.session_state.err.get('step1'):
        st.error(st.session_state.err['step1'])
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c2:
        if st.button("Continue →", type="primary", use_container_width=True):
            if not st.session_state.sizeA:
                set_err('step1', "Please select a squad size to continue.")
                st.rerun()
            else:
                clear_err('step1')
                go_to(2)

# ═══════════════════════════════════════════════════════════════
# STEP 2 — Team B Squad Size
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="d11-steplabel">Step 2 of 6 — Squad Size</div>', unsafe_allow_html=True)
    st.markdown('<div class="d11-card team-b">', unsafe_allow_html=True)
    st.markdown('<span class="d11-badge badge-b">TEAM B</span> **How many players?**', unsafe_allow_html=True)
    st.caption("Select squad size for Team B")

    cols = st.columns(len(SIZES))
    for i, n in enumerate(SIZES):
        selected = st.session_state.sizeB == n
        if cols[i].button(f"{n}\nPlayers", key=f"sizeB_{n}", type="primary" if selected else "secondary", use_container_width=True):
            st.session_state.sizeB = n
            st.rerun()

    if st.session_state.err.get('step2'):
        st.error(st.session_state.err['step2'])
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back", use_container_width=True):
            go_to(1)
    with c3:
        if st.button("Continue →", type="primary", use_container_width=True):
            if not st.session_state.sizeB:
                set_err('step2', "Please select a squad size to continue.")
                st.rerun()
            else:
                clear_err('step2')
                go_to(3)

# ═══════════════════════════════════════════════════════════════
# STEP 3 — Player Details
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown('<div class="d11-steplabel">Step 3 of 6 — Player Details</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="d11-info">
      Assign roles: <strong>WK</strong> = Wicket Keeper &nbsp;|&nbsp; <strong>BAT</strong> = Batsman &nbsp;|&nbsp;
      <strong>ALL</strong> = All-Rounder &nbsp;|&nbsp; <strong>BOWL</strong> = Bowler<br>
      Min 1 of each role per team · Final squad = 6 from batting team + 5 from bowling team
    </div>
    """, unsafe_allow_html=True)

    # ensure input state lists exist with right length, preserving prior values
    def ensure_inputs(team, size):
        name_key = f"names_{team}"
        role_key = f"roles_{team}"
        if name_key not in st.session_state:
            st.session_state[name_key] = [""] * size
        if role_key not in st.session_state:
            st.session_state[role_key] = [""] * size
        # resize while preserving existing values
        cur_names = st.session_state[name_key]
        cur_roles = st.session_state[role_key]
        if len(cur_names) != size:
            new_names = (cur_names + [""] * size)[:size]
            new_roles = (cur_roles + [""] * size)[:size]
            st.session_state[name_key] = new_names
            st.session_state[role_key] = new_roles

    ensure_inputs('A', st.session_state.sizeA)
    ensure_inputs('B', st.session_state.sizeB)

    def render_team_inputs(team, size, badge_class, badge_label):
        st.markdown(f'<div class="d11-card team-{team.lower()}">', unsafe_allow_html=True)
        st.markdown(f'<span class="d11-badge {badge_class}">{badge_label}</span> **Player Details**', unsafe_allow_html=True)
        name_key = f"names_{team}"
        role_key = f"roles_{team}"
        for i in range(size):
            c1, c2, c3 = st.columns([0.5, 3, 2])
            c1.markdown(f"<div style='text-align:center;color:var(--muted);font-family:Orbitron,sans-serif;font-size:0.75rem;padding-top:8px;'>{i+1}</div>", unsafe_allow_html=True)
            st.session_state[name_key][i] = c2.text_input(
                "Player name", value=st.session_state[name_key][i],
                key=f"{team}_name_{i}", label_visibility="collapsed", placeholder="Player name"
            )
            role_options = [""] + ROLES
            cur_role = st.session_state[role_key][i]
            idx = role_options.index(cur_role) if cur_role in role_options else 0
            st.session_state[role_key][i] = c3.selectbox(
                "Role", role_options, index=idx, key=f"{team}_role_{i}", label_visibility="collapsed"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    render_team_inputs('A', st.session_state.sizeA, 'badge-a', 'TEAM A')
    render_team_inputs('B', st.session_state.sizeB, 'badge-b', 'TEAM B')

    if st.session_state.err.get('step3'):
        st.error(st.session_state.err['step3'])

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back", use_container_width=True, key="back_step3"):
            go_to(2)
    with c3:
        if st.button("Continue →", type="primary", use_container_width=True, key="next_step3"):
            playersA = [{'name': n.strip(), 'role': r, 'team': 'A'}
                        for n, r in zip(st.session_state['names_A'], st.session_state['roles_A'])]
            playersB = [{'name': n.strip(), 'role': r, 'team': 'B'}
                        for n, r in zip(st.session_state['names_B'], st.session_state['roles_B'])]
            if not validate_players(playersA) or not validate_players(playersB):
                set_err('step3', "Please fill all player names, assign all roles, and ensure each "
                                  "team has at least 1 WK, BAT, ALL & BOWL.")
                st.rerun()
            else:
                clear_err('step3')
                st.session_state.playersA = playersA
                st.session_state.playersB = playersB
                go_to(4)

# ═══════════════════════════════════════════════════════════════
# STEP 4 — Number of Dream11 Teams
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    st.markdown('<div class="d11-steplabel">Step 4 of 6 — Number of Teams</div>', unsafe_allow_html=True)
    st.markdown('<div class="d11-card gold-top">', unsafe_allow_html=True)
    st.markdown("**🎯 How Many Dream11 Teams?**")
    st.caption("Each generated team will have at least 2 unique players different from every other team — no duplicates! "
                "Max teams depend on your squad sizes. The app will warn you if uniqueness can't be satisfied.")

    counts = list(range(2, 12))
    row1, row2 = counts[:5], counts[5:]
    for row in (row1, row2):
        cols = st.columns(len(row))
        for i, n in enumerate(row):
            selected = st.session_state.numTeams == n
            if cols[i].button(f"{n}", key=f"count_{n}", type="primary" if selected else "secondary", use_container_width=True):
                st.session_state.numTeams = n
                st.rerun()

    if st.session_state.err.get('step4'):
        st.error(st.session_state.err['step4'])
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back", use_container_width=True, key="back_step4"):
            go_to(3)
    with c3:
        if st.button("Continue →", type="primary", use_container_width=True, key="next_step4"):
            if not st.session_state.numTeams:
                set_err('step4', "Please select how many teams to generate.")
                st.rerun()
            else:
                clear_err('step4')
                go_to(5)

# ═══════════════════════════════════════════════════════════════
# STEP 5 — Toss / Bat First
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    st.markdown('<div class="d11-steplabel">Step 5 of 6 — Toss</div>', unsafe_allow_html=True)
    st.markdown('<div class="d11-card">', unsafe_allow_html=True)
    st.markdown("**⚡ Who Bats First?**")
    st.caption("Batting-first team gets 6 players · Bowling team gets 5 players")

    c1, c2 = st.columns(2)
    with c1:
        selected = st.session_state.batFirst == 'A'
        if st.button("🏏 Team A\nBats First", key="batA", type="primary" if selected else "secondary", use_container_width=True):
            st.session_state.batFirst = 'A'
            st.rerun()
    with c2:
        selected = st.session_state.batFirst == 'B'
        if st.button("🏏 Team B\nBats First", key="batB", type="primary" if selected else "secondary", use_container_width=True):
            st.session_state.batFirst = 'B'
            st.rerun()

    if st.session_state.err.get('step5'):
        st.error(st.session_state.err['step5'])
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back", use_container_width=True, key="back_step5"):
            go_to(4)
    with c3:
        if st.button("Generate Teams ✦", type="primary", use_container_width=True, key="gen_step5"):
            if not st.session_state.batFirst:
                set_err('step5', "Please select which team bats first.")
                st.rerun()
            else:
                clear_err('step5')
                generate_all_teams()
                go_to(6)

# ═══════════════════════════════════════════════════════════════
# STEP 6 — Results
# ═══════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    teams = st.session_state.generatedTeams
    bat_first = st.session_state.batFirst
    label_bat = 'Team A' if bat_first == 'A' else 'Team B'

    st.markdown(f"""
    <div style="text-align:center;padding:10px 0 20px;">
      <h2 style="color:var(--gold);letter-spacing:5px;">⚡ YOUR DREAM TEAMS</h2>
      <p style="color:var(--muted);letter-spacing:2px;font-size:0.85rem;">
        {label_bat} bats first · {len(teams)} unique team(s) generated
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not teams:
        st.info("No teams were generated. Go back and adjust your settings.")
    else:
        tab_labels = [f"T{i+1}" for i in range(len(teams))]
        tabs = st.tabs(tab_labels)

        for idx, tab in enumerate(tabs):
            with tab:
                team = teams[idx]
                sel1, sel2 = team['sel1'], team['sel2']
                # sel1 = batPool selection, sel2 = bowlPool selection test
                if bat_first == 'A':
                    team_a_players, team_b_players = sel1, sel2
                    a_is_batting = True
                else:
                    team_a_players, team_b_players = sel2, sel1
                    a_is_batting = False

                col_a, col_b = st.columns(2)

                def render_team_panel(col, players, label, cls, is_batting):
                    with col:
                        flag = '<span class="batting-flag">🏏 BATTING FIRST</span>' if is_batting else ''
                        st.markdown(f'<div class="d11-result-name {cls}">{label} '
                                    f'<small style="font-size:0.65rem;color:var(--muted);">({len(players)} players)</small>{flag}</div>',
                                    unsafe_allow_html=True)
                        for p in players:
                            is_cap = p is team['captain']
                            is_vc = p is team['vc']
                            cap_html = '<span class="captain-badge">C</span>' if is_cap else ''
                            vc_html = '<span class="vc-badge">VC</span>' if is_vc else ''
                            color = ROLE_COLORS[p['role']]
                            st.markdown(
                                f'<div class="d11-player-row">'
                                f'<span>{p["name"]}{cap_html}{vc_html}</span>'
                                f'<span class="role-pill" style="background:{color}22;color:{color};">{p["role"]}</span>'
                                f'</div>', unsafe_allow_html=True
                            )

                render_team_panel(col_a, team_a_players, 'Team A', 'a', a_is_batting)
                render_team_panel(col_b, team_b_players, 'Team B', 'b', not a_is_batting)

                # composition summaries
                counts = {r: sum(1 for p in team['combined'] if p['role'] == r) for r in ROLES}
                chips = "".join(
                    f'<span class="d11-chip" style="background:{ROLE_COLORS[r]}22;color:{ROLE_COLORS[r]};">{r}: {counts[r]}</span>'
                    for r in ROLES
                )
                st.markdown(
                    f'<div style="padding:14px 0 4px;border-top:1px solid var(--border);margin-top:10px;">'
                    f'<span style="color:var(--muted);font-size:0.75rem;letter-spacing:1px;display:block;margin-bottom:6px;">COMPOSITION</span>'
                    f'{chips}'
                    f'<span style="margin-left:8px;color:var(--muted);font-size:0.8rem;">Total: {len(team["combined"])}</span>'
                    f'</div>', unsafe_allow_html=True
                )

                # diff vs previous teams
                if idx > 0:
                    prev = teams[idx - 1]
                    prev_names = {p['name'] for p in prev['combined']}
                    diff_players = [p for p in team['combined'] if p['name'] not in prev_names]
                    tags = "".join(f'<span class="d11-diff-tag">{p["name"]}</span>' for p in diff_players)
                    st.markdown(
                        f'<div style="font-size:0.8rem;color:var(--muted);text-align:center;padding:10px;">'
                        f'<span style="margin-right:6px;">🔄 {len(diff_players)} unique vs T{idx}:</span>{tags}'
                        f'</div>', unsafe_allow_html=True
                    )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↻ REGENERATE ALL TEAMS", use_container_width=True, type="primary"):
            generate_all_teams()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⟵ Start Over", use_container_width=True):
        for key in ['step', 'sizeA', 'sizeB', 'numTeams', 'batFirst', 'playersA', 'playersB',
                    'generatedTeams', 'err', 'names_A', 'names_B', 'roles_A', 'roles_B']:
            st.session_state.pop(key, None)
        init_state()
        go_to(1)