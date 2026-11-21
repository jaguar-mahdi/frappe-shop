# سجل التعلّم (`Learning Log`)

كل مهمة تنتهي بإدخال جديد في آخر هذا الملف. التنسيق موضَّح في [git-workflow.md](git-workflow.md#learning-log-format).

---

## 2026-11-18 — إضافة `CLAUDE.md` وسجل التعلّم وتثبيت `GitHub Spec Kit`

### ما الذي أُنجز ولماذا

- أُنشئ فرع جديد `chore/claude-and-spec-kit` من `main` المحدَّث، لأن `main` محمي بـ`Ruleset` ولا يُسمح بالعمل عليه مباشرة.
- أُنشئ `CLAUDE.md` في جذر المستودع: قواعد دائمة يقرؤها `Claude Code` في بداية كل جلسة.
- أُنشئ `docs/git-workflow.md` لحمل التفاصيل الطويلة حتى يبقى `CLAUDE.md` قصيراً.
- أُنشئ هذا الملف `docs/learning-log.md`.
- ثُبِّتت أداة `specify` (واجهة سطر الأوامر `CLI` = `Command Line Interface` لـ`Spec Kit`) بالإصدار المثبَّت `v1.4.2` عبر `uv`، ثم هُيِّئ `Spec Kit` في المستودع لـ`Claude Code`. لم يُكتب `constitution` ولا `spec` ولا `plan` ولا `tasks` بعد، فقط الهيكل (`scaffolding`).
- أُضيف `.claude/settings.local.json` إلى `.gitignore`.

`Spec Kit` أداة من `GitHub` لأسلوب `SDD` (`Spec-Driven Development` = التطوير المدفوع بالمواصفات): تكتب أولاً "ماذا ولماذا" (`spec`)، ثم "كيف" (`plan`)، ثم قائمة مهام (`tasks`)، ثم التنفيذ.

---

### الأوامر بالتفصيل

#### 1) الدخول إلى المستودع والتحقق من حالته

```bash
cd /workspace/development/frappe-bench/apps/frappe_shop && pwd && git status && git remote -v && git branch -a && ls -la
```

- `cd <path>`: الانتقال إلى مجلد المشروع. ضروري لأن `/workspace/development` مستودع آخر (`frappe_docker`).
- `&&`: نفّذ الأمر التالي فقط إذا نجح السابق.
- `pwd` (`print working directory`): يطبع المجلد الحالي للتأكد.
- `git status`: يعرض الفرع الحالي وهل توجد تعديلات غير محفوظة.
- `git remote -v`: يعرض عناوين المستودع البعيد (`remote`) المسمى `origin`. `-v` = `verbose`.
- `git branch -a`: يعرض كل الفروع المحلية والبعيدة. `-a` = `all`.
- `ls -la`: يعرض كل الملفات، ومنها المخفية (`-a`)، بتفاصيلها (`-l`).

**المخرجات:** المجلد صحيح، و`origin` يشير إلى `jaguar-mahdi/frappe-shop`، والشجرة نظيفة (`working tree clean`). **لكن** الفرع الحالي كان `ci/dependabot-config` وليس `main` كما كان متوقعاً.

#### 2) تشخيص الفرع غير المتوقع

```bash
git fetch origin --prune
git log --oneline -5 main
git log --oneline -5 origin/main
git log --oneline -5 ci/dependabot-config
git rev-list --left-right --count main...origin/main
git diff --stat origin/main ci/dependabot-config
```

- `git fetch origin`: ينزّل آخر حالة من `GitHub` دون أن يغيّر ملفاتك أو فروعك المحلية.
- `--prune`: يحذف المراجع المحلية لفروع بعيدة حُذفت من `GitHub`.
- `git log --oneline -5 <ref>`: آخر 5 `commits`، كل واحد في سطر.
- `git rev-list --left-right --count A...B`: يعدّ `commits` الموجودة في `A` فقط (يسار) وفي `B` فقط (يمين).
- `git diff --stat A B`: ملخص الفروق في الملفات بين مرجعين.

**المخرجات ومعناها:**
- `[deleted] (none) -> origin/ci/dependabot-config`: الفرع البعيد حُذف بعد دمج الـ`PR` (`Pull Request`).
- `origin/main` فيه `commit` جديد `ci: add dependabot config for actions and pip (#2)`، أي أن الفرع دُمج بـ`squash merge` في `PR #2`.
- `0	1`: `main` المحلي متأخر بـ`commit` واحد عن `origin/main`، وليس فيه شيء غير موجود على `GitHub`.
- `git diff --stat` لم يطبع شيئاً: محتوى الفرع القديم مطابق تماماً لـ`origin/main`، فلا عمل ضائع.

**الجذر:** بعد `squash merge` يصنع `GitHub` `commit` جديداً على `main`، فيبقى الفرع المحلي القديم كما هو ويبقى `main` المحلي متأخراً حتى تسحبه بنفسك.

#### 3) تحديث `main` وإنشاء الفرع الجديد

```bash
git switch main
git pull --ff-only origin main
git switch -c chore/claude-and-spec-kit
```

- `git switch main`: الانتقال إلى فرع `main`.
- `git pull origin main`: يجلب `main` من `origin` ويدمجه في الفرع المحلي.
- `--ff-only` (`fast-forward only`): يقبل التحديث فقط إذا أمكن "تقديم المؤشر" دون إنشاء `merge commit`، ويفشل بدل أن يخلط التاريخ. هذا يتماشى مع `linear history`.
- `git switch -c <name>`: ينشئ فرعاً جديداً (`-c` = `create`) من النقطة الحالية وينتقل إليه.

**المخرجات:** `Fast-forward` مع إضافة `.github/dependabot.yml`، ثم `Switched to a new branch 'chore/claude-and-spec-kit'`.

> الفرع المحلي القديم `ci/dependabot-config` ما زال موجوداً. يمكن حذفه لاحقاً بـ`git branch -d ci/dependabot-config` (الخيار `-d` يرفض الحذف إن لم يكن مدموجاً، و`-D` يفرضه). بعد `squash merge` قد يحتاج `-D` لأن `git` لا يرى الـ`commits` نفسها في `main`.

#### 4) فحص الإعدادات والأدوات

```bash
cat .pre-commit-config.yaml; cat .gitignore; ls .github .github/*
which uv uvx pre-commit python3 git; uv --version; pre-commit --version; python3 --version
```

- `cat`: يطبع محتوى ملف.
- `which`: يبيّن مسار البرنامج الذي سيُنفَّذ.
- `--version`: يطبع الإصدار.

**المخرجات:** `uv 0.13.8` و`pre-commit 4.7.0` و`Python 3.14.10` موجودة في `~/.local/bin`. خطافات `pre-commit` هي: `pre-commit-hooks` (مسافات زائدة، `JSON`، `YAML`، `TOML`...)، و`ruff` (ترتيب الاستيراد وفحص `Python` وتنسيقه)، و`prettier`، و`eslint`.

#### 5) قراءة تعليمات `Spec Kit` الرسمية

قُرئ المستودع الرسمي `github/spec-kit` (`README` و`docs/installation.md` و`docs/integrations/claude.md` وصفحة `Releases`) بدلاً من الاعتماد على الذاكرة. أهم ما تبيّن:
- آخر إصدار هو `v1.4.2`.
- أصبحت الأوامر بصيغة `/speckit-<name>` بشَرطة (`-`) بدل النقطة القديمة `/speckit.<name>`.
- لـ`Claude` تُثبَّت `skills` في `.claude/skills/` (ولم تعد `.claude/commands/`).
- الخيار القديم `--ai` استُبدل بـ`--integration`.

#### 6) التحقق من وجود `claude` و`specify`

```bash
which claude specify; uv tool list; git config --global core.excludesfile; git check-ignore -v .ruff_cache
```

- `uv tool list`: يعرض الأدوات المثبَّتة عبر `uv tool install`.
- `git check-ignore -v <path>`: يخبرك هل `git` يتجاهل المسار وبسبب أي قاعدة.

**المخرجات:** `Exit code 1` مع عرض `pre-commit` فقط ضمن `uv tool list`.

**هل هذا خطأ؟** لا. `which` يعيد `1` إذا لم يجد أحد البرامج، و`git check-ignore` يعيد `1` إذا لم يكن المسار متجاهَلاً. المعنى:
- `claude` غير موجود في `PATH`، لأن امتداد `VS Code` يحمل نسخته الخاصة. لذلك احتجنا لاحقاً إلى `--ignore-agent-tools`.
- `specify` غير مثبَّت بعد.
- `.ruff_cache` لا تظهر في `git status` رغم أنها غير مذكورة في `.gitignore`، لأن `ruff` ينشئ داخلها ملف `.gitignore` خاصاً بها يحتوي `*` (تأكدنا بـ`cat .ruff_cache/.gitignore`).

#### 7) تثبيت `specify` بإصدار مثبَّت

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.4.2
specify version
```

- `uv tool install`: يثبّت أداة `Python` في بيئة معزولة خاصة بها (لا تختلط بحزم `bench`)، ويضع ملفها التنفيذي في `~/.local/bin`.
- `specify-cli`: اسم الحزمة.
- `--from git+<url>@v1.4.2`: ثبّت من مستودع `git` عند الوسم (`tag`) `v1.4.2` تحديداً، وهذا هو "الشكل الصريح" بدل أحدث إصدار متغيّر. التوثيق يطلب إبقاء حرف `v` في الوسم.
- `specify version`: يعرض الإصدار المثبَّت للتأكد.

**المخرجات:** `specify-cli==1.4.2 (from ...@1e421b58...)`، أي أن الوسم يشير إلى ذلك الـ`commit`. ثم `Installed 1 executable: specify`، و`CLI Version 1.4.2`.

> هذا التثبيت خارج المستودع (`~/.local/bin`) ولا يُرفع إلى `GitHub`. داخل حاوية جديدة ستحتاج إلى إعادة تشغيل الأمر نفسه.

#### 8) قراءة خيارات `init`

```bash
specify init --help
```

يعرض الخيارات الحالية للإصدار المثبَّت، للتأكد من أنها تطابق التوثيق.

#### 9) تهيئة `Spec Kit`

```bash
specify init --here --force --non-interactive --integration claude --script sh --ignore-agent-tools
```

- `--here`: هيّئ في المجلد الحالي بدل إنشاء مجلد جديد.
- `--force`: تخطَّ سؤال التأكيد لأن المجلد غير فارغ. قد يستبدل الملفات التي يديرها `Spec Kit` فقط، ولهذا نفّذناه وشجرة العمل نظيفة على فرع جديد حتى تظهر أي تغييرات في `git status`.
- `--non-interactive`: لا تسأل أي سؤال تفاعلي. بدونه قد يعلق الأمر في انتظار مفاتيح الأسهم.
- `--integration claude`: اختر `Claude Code`. بدونه يكون الافتراضي في الوضع غير التفاعلي `GitHub Copilot`.
- `--script sh`: استخدم سكربتات `bash` (مناسبة لـ`Linux`).
- `--ignore-agent-tools`: لا تتحقق من وجود البرنامج `claude` في `PATH` (انظر الخطوة 6).

**المخرجات:** كل المراحل `ok`، و`Project ready.`، إضافة إلى تحذير `Agent Folder Security` بأن بعض الوكلاء قد يخزّنون بيانات اعتماد في مجلدهم. ولهذا أضفنا `.claude/settings.local.json` إلى `.gitignore`، وهو الملف الذي يحفظ فيه `Claude Code` الأذونات الشخصية المحلية.

#### 10) مراجعة ما أُنشئ قبل الحفظ

```bash
git status --short
find .specify .claude -type f | sort
cat .specify/.gitignore .specify/init-options.json .specify/integration.json
grep -rniE "/workspace|/home/|password|secret|token|api[_-]?key|@gmail" .specify .claude
```

- `git status --short`: حالة مختصرة. `??` تعني ملفاً غير متتبَّع (`untracked`).
- `find <dirs> -type f`: يسرد الملفات فقط.
- `grep -rniE`: بحث تكراري (`-r`)، غير حساس لحالة الأحرف (`-i`)، مع أرقام الأسطر (`-n`)، بتعبير نمطي موسَّع (`-E`)، عن أي سرّ أو مسار شخصي.

**المخرجات:** ظهر مجلدان جديدان فقط، `.claude/` و`.specify/`، ولم يُعدَّل أي ملف موجود. لم يُنشأ `.claude/settings.json`، أي لا توجد `hooks`. نتائج `grep` كلها نصوص عامة في القوالب (مثل `reset their password` كمثال)، لا أسرار فيها ولا مسارات شخصية. ملف `constitution.md` قالب فارغ بعناصر نائبة مثل `[PROJECT_NAME]`.

#### 11) فحص `git hooks` وملفات `CI`

```bash
ls .git/hooks | grep -v sample
grep -nE "name:|run:|pre-commit|branches" .github/workflows/*.yml
```

- `grep -v sample`: اعرض كل شيء ما عدا ملفات الأمثلة.

**المخرجات:** يوجد `pre-commit` في `.git/hooks`، أي أن الفحوص تعمل تلقائياً عند كل `git commit`. أما `Frappe Linter` فيستخدم `pre-commit/action` في `CI` (`Continuous Integration` = التكامل المستمر).

#### 12) تعديل `.gitignore` وتجهيز الملفات وتشغيل `pre-commit`

```bash
printf '\n# Claude Code personal settings (local permissions, never shared)\n.claude/settings.local.json\n' >> .gitignore
git add CLAUDE.md docs/git-workflow.md .gitignore .specify .claude
pre-commit run --all-files
```

- `printf '...' >> .gitignore`: يضيف نصاً إلى آخر الملف. `>>` تعني "أضِف"، أما `>` فتمسح الملف وتكتب من جديد.
- `git add <paths>`: يضع الملفات في منطقة التجهيز (`staging area`).
- `pre-commit run --all-files`: يشغّل كل الخطافات على كل الملفات المتتبَّعة، وهو ما يفعله `CI`. **مهم:** يفحص فقط ما يعرفه `git`، لذلك أضفنا الملفات الجديدة بـ`git add` أولاً، وإلا لتجاهلها الفحص.

**المخرجات:** كل الخطافات `Passed`، و`prettier` و`eslint` كانت `Skipped` لعدم وجود ملفات `JavaScript`. `exit=0` يعني نجاحاً.

#### 13) الحفظ في `commits` منطقية ثم الرفع

```bash
git add docs/learning-log.md
git commit -m "docs: add CLAUDE.md, git workflow guide and learning log" -- CLAUDE.md docs/
git commit -m "chore: add GitHub Spec Kit v1.4.2 scaffolding for Claude Code"
pre-commit run --all-files
git push -u origin chore/claude-and-spec-kit
```

- `git commit -m "<msg>" -- <paths>`: يحفظ فقط المسارات المحددة بعد `--`، وتبقى بقية الملفات مجهَّزة للـ`commit` التالي. بهذا انفصل التوثيق عن `Spec Kit`.
- الـ`commit` الثاني بلا مسارات يحفظ كل ما تبقى في منطقة التجهيز.
- `git push -u origin <branch>`: يرفع الفرع إلى `GitHub`. الخيار `-u` (`--set-upstream`) يربط الفرع المحلي بالبعيد، فيكفي بعده `git push` و`git pull` دون أسماء.

**مخرجات الـ`commits`:**
- `9d2d95c docs: add CLAUDE.md, git workflow guide and learning log` (3 ملفات).
- `0ec3186 chore: add GitHub Spec Kit v1.4.2 scaffolding for Claude Code` (30 ملفاً، منها `.gitignore`).
- في الـ`commit` الأول ظهر `[WARNING] Unstaged files detected` ثم `Stashing unstaged files` ثم `Restored changes`. **هذا ليس خطأ.** عند استخدام `git commit -- <paths>` يحفظ `git` المسارات المحددة فقط، فيرى خطاف `pre-commit` بقية الملفات المجهَّزة كأنها "غير مجهَّزة". لذلك خبّأها مؤقتاً (`stash`)، وفحص ملفات هذا الـ`commit` وحدها، ثم أعادها كما كانت. وتأكدنا بـ`git show --stat <hash>` أن كل `commit` يحوي الملفات الصحيحة.
- `pre-commit run --all-files` بعد الـ`commits`: كل الخطافات `Passed` و`exit=0`.

**مخرجات `git push`:**
- `* [new branch] chore/claude-and-spec-kit -> chore/claude-and-spec-kit`: أُنشئ الفرع على `GitHub`.
- `branch 'chore/claude-and-spec-kit' set up to track 'origin/chore/claude-and-spec-kit'`: هذا أثر `-u`.
- أعطى `GitHub` رابطاً لفتح الـ`PR`: `https://github.com/jaguar-mahdi/frappe-shop/pull/new/chore/claude-and-spec-kit`.

#### 14) تحديث هذا السجل ورفعه

```bash
git add docs/learning-log.md
git commit -m "docs: record push results in learning log"
pre-commit run --all-files
git push
```

- بعد `-u` في الرفع الأول يكفي `git push` وحده، لأن الفرع صار مربوطاً بـ`origin/chore/claude-and-spec-kit`.
- كل `push` جديد إلى فرع له `PR` مفتوح يعيد تشغيل فحوص `CI`.
- عند `squash merge` ستُدمج الـ`commits` الثلاثة في `commit` واحد على `main` يحمل عنوان الـ`PR`.

### الخطوات التالية

1. افتح الـ`PR` من الرابط أعلاه، وانتظر نجاح `Server` و`Frappe Linter` و`Vulnerable Dependency Check`، ثم ادمج بـ`squash`.
2. بعد الدمج: `git switch main && git pull --ff-only origin main`.
3. في جلسة `Claude Code` جديدة: ابدأ بـ`/speckit-constitution`.

---

## 2026-11-21 — `SDD` المرحلة 1: `constitution` و`spec` لميزة "Book catalog"

### ما الذي أُنجز ولماذا

- كُتب "دستور" المشروع `.specify/memory/constitution.md` بالإصدار `1.0.0`، وفيه المبادئ الخمسة التي قرّرها المسؤول عن المشروع (`maintainer`) نصاً، دون إضافة مبادئ منتج جديدة. القسمان `Platform Constraints` و`Development Workflow` ينقلان قرارات موجودة أصلاً في `CLAUDE.md`.
- كُتبت مواصفة الميزة الأولى `specs/001-book-catalog/spec.md` (إصدار المتجر `0.1.0`) وقائمة الجودة `checklists/requirements.md`.
- لم يُكتب `plan` ولا `tasks` ولا كود.
- أُضيف سطر إلى `CLAUDE.md` يشرح كيف تُطابَق مجلدات `Spec Kit` مع تسمية الفروع.

`SDD` = `Spec-Driven Development`. و`SemVer` = `Semantic Versioning`، أي ترقيم الإصدارات بصيغة `MAJOR.MINOR.PATCH`.

### الأوامر بالتفصيل

#### 1) الدخول والتحديث

```bash
cd /workspace/development/frappe-bench/apps/frappe_shop && pwd && git status -sb | head -3 && git fetch origin --prune
git log --oneline -5 origin/main; git branch -a
git pull --ff-only origin main
```

- `git status -sb`: حالة مختصرة (`-s` = `short`) مع سطر الفرع ومقارنته بالبعيد (`-b` = `branch`).
- `| head -3`: اعرض أول 3 أسطر فقط.

**المخرجات:** كنا على `main`، و`[deleted] ... origin/chore/claude-and-spec-kit` يعني أن الـ`PR` السابق دُمج وحُذف فرعه. ظهر في `origin/main` الـ`commit` `chore: add CLAUDE.md, learning log and GitHub Spec Kit scaffolding (#9)`، وهو `commit` واحد لأن الدمج تم بـ`squash`. أما `git pull --ff-only` فأعاد `Already up to date`.

#### 2) قراءة ملفات `Spec Kit`

```bash
cat CLAUDE.md .specify/memory/constitution.md .claude/skills/speckit-constitution/SKILL.md .claude/skills/speckit-specify/SKILL.md
ls .specify; ls .specify/extensions*
sed -n 1,80p .specify/scripts/bash/create-new-feature.sh
```

- `sed -n 1,80p <file>`: اطبع الأسطر من 1 إلى 80 فقط. `-n` تمنع الطباعة التلقائية، و`p` تعني `print`.

**المخرجات ومعناها:** لا يوجد `.specify/extensions.yml`، أي أن إضافة (`extension`) الـ`git` غير مثبَّتة. ولذلك لا يوجد `hook` من نوع `before_specify` ينشئ فرعاً، ومهارة `speckit-specify` تنشئ مجلد `specs/` فقط. **الخلاصة:** `Spec Kit` لن ينشئ فرعاً باسم خاص به، فأنشأنا الفرع يدوياً بالاسم الصحيح من البداية، ولم نحتج إلى إعادة تسمية.

#### 3) إنشاء الفرع وتحليل القالب

```bash
git switch -c docs/001-book-catalog-spec
.specify/scripts/bash/resolve-template.sh constitution-template --json
grep -nE "git (checkout|switch|branch)" .specify/scripts/bash/*.sh
cat frappe_shop/__init__.py
```

- `resolve-template.sh constitution-template --json`: خطوة تطلبها المهارة. تدمج طبقات القوالب (`overrides` و`presets` و`extensions`) وتعيد القالب النهائي بصيغة `JSON`.
- `grep -nE ...`: يبحث هل تنشئ سكربتات `Spec Kit` فروعاً بنفسها.
- `frappe_shop/__init__.py`: فيه `__version__` الخاص بالتطبيق.

**المخرجات:** `exit=0` والقالب نفسه الموجود على القرص، أي لا توجد طبقات إضافية. `grep` لم يجد شيئاً، أي أن السكربتات لا تمسّ الفروع. والتطبيق حالياً `__version__ = "0.0.1"`. الانتقال إلى `0.1.0` يحدث عند إصدار الميزة، وليس في هذه المرحلة.

#### 4) كتابة `constitution` والتحقق

```bash
grep -nE "\[[A-Z_]+\]" .specify/memory/constitution.md
```

يبحث عن أي عنصر نائب بقي بصيغة `[ALL_CAPS]`. **المخرجات:** لا شيء مع `exit=1`. هنا `exit=1` يعني "لم يُعثر على تطابق"، وهي النتيجة المطلوبة.

- لم يُترك تقرير `Sync Impact Report` في الملف، لأن المهارة تقول إنه مسودة مؤقتة تُحذف قبل الـ`commit`. ملخصه: الإصدار من `template` إلى `1.0.0`، وأُضيفت المبادئ `I`–`V` والأقسام `Platform Constraints` و`Development Workflow` و`Governance`، ولا يوجد `TODO`.

#### 5) أسئلة التوضيح قبل كتابة `spec`

طُرحت 7 أسئلة في جولتين، لأن تفاصيل المنتج قرارك وليست قراري. الإجابات:
- البحث عن الكاتب: `filter` و`search` معاً.
- كاتب واحد لكل كتاب.
- الحقول الخمسة كلها إلزامية.
- `ISBN` فريد بلا فحص للصيغة.
- اللغة نص حر (`free text`).
- كتب العرض كلاسيكيات من الملكية العامة (`public domain`)، مع سعر ومخزون.

سُجِّلت في قسم `Clarifications` داخل `spec.md`.

#### 6) إنشاء مجلد الميزة

```bash
mkdir -p specs/001-book-catalog/checklists
printf '{\n  "feature_directory": "specs/001-book-catalog"\n}\n' > .specify/feature.json
git check-ignore -v .specify/feature.json
```

- `mkdir -p`: ينشئ المجلد ومجلداته الأب إن لم تكن موجودة، ولا يعطي خطأً إن كان موجوداً.
- `.specify/feature.json`: مؤشر محلي تستخدمه `/speckit-plan` و`/speckit-tasks` لمعرفة الميزة الحالية.
- `git check-ignore -v`: **المخرجات** `.specify/.gitignore:6:feature.json`، أي أن الملف متجاهَل عن قصد لأنه حالة خاصة بالجهاز، ولن يُرفع.

#### 7) التجهيز والفحص

```bash
ls .specify/extensions.yml
git add .specify/memory/constitution.md specs CLAUDE.md
pre-commit run --all-files
```

- `ls .specify/extensions.yml` أعاد `No such file or directory`. هذا متوقع، ويعني أنه لا توجد `post-hooks` بعد `specify`.
- `pre-commit`: كل الخطافات `Passed` و`exit=0`.

#### 8) الـ`commits` والرفع

```bash
git commit -m "docs: ratify project constitution v1.0.0" -- .specify/memory/constitution.md
git commit -m "docs: add book catalog specification (001)" -- specs/
git add docs/learning-log.md
git commit -m "docs: map Spec Kit branches in CLAUDE.md and update learning log"
pre-commit run --all-files
git push -u origin docs/001-book-catalog-spec
```

- كل `commit` يحمل جزءاً منطقياً واحداً، لأن `--` تحدّد المسارات.
- نوع الـ`commit` هو `docs` لأن التغييرات كلها وثائق، بلا كود.

**مخرجات الـ`commits`:**
- `72fac9c docs: ratify project constitution v1.0.0` (ملف واحد).
- `091ed91 docs: add book catalog specification (001)` (ملفان).
- `0da9f92 docs: map Spec Kit branches in CLAUDE.md and update learning log` (ملفان).
- `pre-commit` بعدها أعاد `exit=0`.

**مخرجات `git push`:**
- `* [new branch] docs/001-book-catalog-spec -> docs/001-book-catalog-spec`، والفرع مربوط بالبعيد بفضل `-u`.
- رابط فتح الـ`PR`: `https://github.com/jaguar-mahdi/frappe-shop/pull/new/docs/001-book-catalog-spec`.

بعدها سُجِّلت هذه النتائج بـ`git commit -m "docs: record push results in learning log"` ثم `git push`.

### الخطوات التالية

1. راجع الـ`PR`، وخصوصاً قسم `Assumptions` في `spec.md`، ثم ادمجه بـ`squash`.
2. اختياري: `/speckit-clarify` لتأكيد الافتراضات.
3. ثم `/speckit-plan` على فرع جديد، مثل `docs/001-book-catalog-plan`.

---

## 2026-11-21 — `SDD` المرحلة 2: `plan` ثم `tasks` ثم `implement` لميزة "Book catalog"

### ما الذي أُنجز ولماذا

- `/speckit-plan`: كُتبت ملفات `plan.md` و`research.md` و`data-model.md` و`contracts/server-interfaces.md` و`quickstart.md`. نجحت الخطة في `Constitution Check` (`v1.0.0`).
- كشف البحث تعارضين بين الـ`spec` وما يسمح به `webshop` في إعداداته القياسية، فطُرحت 4 أسئلة على المسؤول عن المشروع (`maintainer`). القرارات:
  - المؤلف صار `Link` إلى `DocType` جديد اسمه `Book Author`.
  - الطلب مباشر (`Place Order`) مع `override` صغير يخفي زر `Pay`.
  - سعر كل كتاب 15,000 مع 20 نسخة في المخزون.
  - قائمة الكتب العشرة بقيم تجريبية (`demo`).
  - حُدِّثت الـ`spec` بقسم `Clarifications` جديد.
- `/speckit-tasks`: ملف `tasks.md` فيه 25 مهمة مرتبة حسب `user story`.
- `/speckit-implement`: نُفِّذت المهام كلها، ثم تُحقِّق منها على الموقع، ثم بـ19 اختباراً آلياً.
- تحديث `ci.yml` ليثبّت `payments` و`erpnext` و`webshop`.

### مصطلحات Frappe المستخدمة

- `Custom Field`: حقل يُضاف إلى `DocType` موجود (مثل `Item`) دون تعديل كود `erpnext`.
- `fixtures`: سجلات من قاعدة البيانات تُصدَّر إلى ملفات `JSON` داخل التطبيق، ويعيد `bench migrate` إنشاءها على أي موقع.
- `Property Setter`: يغيّر خاصية في `DocType` موجود، وهنا غيّر `search_fields` لـ`Website Item`.
- `hooks.py`: ملف يخبر Frappe متى يستدعي كودنا:
  - `doc_events`: عند حفظ مستند.
  - `update_website_context`: عند بناء صفحة ويب.
  - `before_tests`: قبل تشغيل الاختبارات.
  - `required_apps`: التطبيقات التي يجب أن تكون مثبَّتة قبل تطبيقنا.

### الأوامر بالتفصيل

#### 1) التحديث وإنشاء الفرع

```bash
cd /workspace/development/frappe-bench/apps/frappe_shop && pwd && git status -sb | head -3 && git fetch origin --prune
git switch main && git pull --ff-only origin main && git switch -c feat/001-book-catalog
```

**المخرجات:** `4981bd6..194c64a main -> origin/main`، أي أن الـ`PR #10` دُمج. ثم `Fast-forward` وإنشاء الفرع. البادئة `feat` لأن هذا الفرع يضيف ميزة.

#### 2) قراءة المهارات والتحقق من الملفات

```bash
sed -n '/^## Outline/,$p' .claude/skills/speckit-plan/SKILL.md      # (و tasks و implement)
git diff --stat ee82fd6 HEAD -- specs .specify/memory CLAUDE.md
.specify/scripts/bash/setup-plan.sh --json
```

- `sed -n '/A/,$p'`: يطبع من أول سطر يطابق `A` حتى نهاية الملف.
- `git diff --stat <old> HEAD -- <paths>`: هل تغيّرت هذه الملفات بين آخر `commit` لنا وبين `main` بعد الدمج؟ لم يطبع شيئاً، أي لم يعدّل أحد الـ`spec` عند الدمج.
- `setup-plan.sh --json`: نسخ قالب `plan.md` وأعاد المسارات بصيغة `JSON`.

#### 3) البحث في كود `webshop` و`frappe` (للقراءة فقط)

```bash
git -C apps/<app> rev-parse --abbrev-ref HEAD; git -C apps/<app> describe --tags --abbrev=0
grep -n "<pattern>" <file>; sed -n A,Bp <file>
```

- `git -C <dir>`: يشغّل `git` كأنك داخل ذلك المجلد، دون `cd`. استُعمل للقراءة فقط.
- `describe --tags --abbrev=0`: أقرب وسم (`tag`) للإصدار. `webshop` ليس له وسوم.

**أهم ما وُجد:**
- `validate_field_filters`: فلاتر `webshop` تقبل حقول `Link` فقط، وهذا سبب قرار `Book Author`.
- `validate_checkout`: `enable_checkout` يُطفأ تلقائياً إذا لم يوجد `payment_gateway_account`.
- `order.html`: زر `Pay` يظهر إذا كان `enabled_checkout` مفعّلاً.
- `post_process_context`: يشغّل `update_website_context` بعد `get_context`، فيمكن للـ`hook` أن يغيّر ما وضعته الصفحة.
- `_get_missing_mandatory_fields`: الخادم يفحص `reqd` فقط، ولا يفحص `mandatory_depends_on`.
- `erpnext` `v16` ليس فيه `before_tests`، واستيراد `erpnext.tests.utils` ينشئ بيانات `_Test` كثيرة.

#### 4) فحص الموقع

```bash
bench --site development.localhost execute frappe.get_all --kwargs '{"doctype":"Company",...}'
bench --site development.localhost execute frappe.db.get_single_value --args '["Webshop Settings","enabled"]'
```

- `bench --site <s> execute <dotted.path>`: يشغّل دالة Python داخل الموقع.
- `--args` تُمرَّر بصيغة `JSON list`، و`--kwargs` بصيغة `JSON object`.

**المخرجات:** الشركة `Nawat` بعملة `IQD`، و`Webshop Settings` غير مُعدّة.

#### 5) خطأ: `Could not find Module: Frappe Shop`

```bash
../env/bin/python <scratchpad>/create_meta.py
```

- **الخطأ:** `frappe.exceptions.LinkValidationError: Could not find Module: Frappe Shop`
- **الجذر:** التطبيق `frappe_shop` لم يكن مثبَّتاً على `development.localhost` (`installed_apps` لم يكن فيه)، فلم يوجد `Module Def` اسمه "Frappe Shop".
- **الحل:**

```bash
bench --site development.localhost install-app frappe_shop
```

`install-app` يتحقق أولاً من `required_apps`. **المخرجات:** `App erpnext already installed` ثم `App webshop already installed` ثم `Installing frappe_shop...`.

#### 6) إنشاء `DocType` و`Custom Fields` و`Property Setter`

السكربت يستخدم `frappe.get_doc({"doctype": "DocType", ...}).insert()` و`create_custom_fields(...)` و`make_property_setter(...)`.
- مع `developer_mode` يكتب Frappe ملفات `book_author.json/.py/.js` داخل التطبيق تلقائياً: `Wrote document file for DocType Book Author`.
- عُيِّن `module = "Frappe Shop"` لكل الحقول حتى يلتقطها فلتر `fixtures`.

#### 7) تصدير `fixtures` و`migrate`

```bash
bench --site development.localhost export-fixtures --app frappe_shop
bench --site development.localhost migrate
```

- `export-fixtures`: يقرأ `fixtures` في `hooks.py` ويكتب `custom_field.json` (8 سجلات) و`property_setter.json` (سجل واحد).
- `migrate`: يطبّق `patches`، ويزامن `DocTypes`، ويستورد `fixtures`. **المخرجات:** `Executing after_migrate hooks...` دون أخطاء.
- تأكدنا من الأعمدة بـ`frappe.db.get_table_columns`: وُجدت `book_author` و`book_isbn` وبقية الحقول.

#### 8) خطأ: `Segmentation fault (core dumped)`، `exit=139`

```bash
/workspace/development/frappe-bench/env/bin/python -X faulthandler -u <scratchpad>/inspect.py
```

- `-X faulthandler`: يطبع مكان الانهيار حتى في `segfault`. أما `-u` فيلغي التخزين المؤقت للمخرجات.
- **الجذر:** سمّيت السكربت `inspect.py`. يضع Python مجلد السكربت أول `sys.path`، فلما استورد `dataclasses` الوحدة القياسية `inspect` حمّل ملفي أنا. نتج استيراد دائري انهار داخل `orjson`. يسمى هذا `module shadowing`.
- **الحل:** إعادة التسمية إلى `site_probe.py`، والتشغيل بـ`python -I` (الوضع المعزول `isolated`، لا يضيف مجلد السكربت إلى `sys.path`).

#### 9) البيانات التجريبية: التشغيل مرتين

```bash
bench --site development.localhost execute frappe_shop.demo.sample_books.create_sample_books   # مرتان
```

**المخرجات:** في المرة الأولى `"created": [10 books]`، وفي الثانية `"created": [], "existing": [10 books]`. هذا يثبت `idempotency`، أي أن تكرار التشغيل آمن.

#### 10) خطأ: `curl` أعاد `000`

```bash
curl -s -o page.html -w '%{http_code}' -H "Host: development.localhost" http://127.0.0.1:8000/all-products
```

- `-w '%{http_code}'`: يطبع رمز `HTTP`. القيمة `000` تعني "لا اتصال".
- `-H "Host: ..."`: يختار الموقع، لأن `bench` يخدم عدة مواقع على المنفذ نفسه.
- **الجذر:** افترضت المنفذ 8000، والحقيقي 8001. هذا مكتوب في `Procfile` (`bench serve --port 8001`) وفي `common_site_config.json`، وأكده `netstat -ltnp`.
- **بعد التصحيح:** `200` للصفحتين. صفحة الكتاب تعرض `DEMO-0003` و`Number of Pages` و`Frappe Books Demo Press`. فلتر `Charles Dickens` أعاد كتابيه فقط، وبحث `wells` أعاد كتابي H. G. Wells.

#### 11) تجربة `Place Order` مع `rollback`

سكربت ينشئ مستخدماً تجريبياً وسلة وعنواناً، ثم يستدعي `place_order()`، ثم ينفّذ `frappe.db.rollback()`.

**المخرجات:**
- `Sales Order` بقيمة `docstatus 1` و`order_type Shopping Cart`.
- `Cash on Delivery [('Cash on Delivery', 'Cash', 100.0)]`.
- `payment requests: 0`.
- الـ`hook` أعاد `{'enabled_checkout': False}`، أي أن `Pay` مخفي.
- بعد `rollback` لم يبقَ المستخدم التجريبي.

#### 12) الاختبارات

```bash
bench --site development.localhost set-config allow_tests true
bench --site development.localhost run-tests --app frappe_shop
```

- `set-config`: يكتب في `site_config.json` المحلي، وهو غير مرفوع إلى `git`. `run-tests` يرفض العمل بدونه حماية للمواقع الحقيقية.
- **فشل أول:** `test_setup_is_idempotent` وجد `brand: '_Test Store Name'`.
  - **الجذر:** اختبار آخر غيّر الاسم، و`rollback` لا يحدث إلا في نهاية الـ`class`، وترتيب الاختبارات أبجدي، فتسرّبت الحالة إلى الاختبار التالي.
  - **الحل:** `self.addCleanup(...)` يعيد القيمة الأصلية.
- **النتيجة:** `Ran 19 tests ... OK`.

#### 13) بروفة `CI` على موقع مؤقت

```bash
bench new-site ci-check.localhost --db-root-password *** --admin-password admin --mariadb-user-host-login-scope='%'
bench --site ci-check.localhost install-app payments      # ثم erpnext ثم webshop ثم frappe_shop
bench --site ci-check.localhost run-tests --app frappe_shop
bench drop-site ci-check.localhost --db-root-password *** --no-backup --force
```

- الغرض: موقع جديد بلا شركة، تماماً مثل `test_site` في `CI`.
- `--mariadb-user-host-login-scope='%'`: ضروري لأن `MariaDB` في حاوية (`container`) أخرى.
- **خطأ ظهر هنا فقط:** `SQL functions are not allowed as strings in SELECT: sum(actual_qty)`.
  - **الجذر:** سطر في الاختبار لا يعمل إلا عندما تُنشأ الكتب لأول مرة. في `development.localhost` كانت الكتب موجودة فلم يُنفَّذ السطر. وFrappe `v16` يمنع دوال `SQL` المكتوبة كنص.
  - **الحل:** الجمع في Python: `sum(frappe.get_all("Bin", ..., pluck="actual_qty"))`.
- **بعدها:** `Ran 19 tests ... OK`، وأنشأ `before_tests` الشركة `Frappe Books Test`. ثم حُذف الموقع ومجلد `archived/sites/ci-check.localhost`.

#### 14) `pre-commit`

```bash
git add -A && pre-commit run --all-files
```

- النتيجة الأولى `ruff-format ... Failed - files were modified by this hook`. **هذا ليس خطأ:** الأداة أعادت تنسيق 4 ملفات وأبلغت بـ`Failed` حتى تراجع التغيير قبل الحفظ.
- بعد `git add -A` وإعادة التشغيل: `exit=0`.

### تغييرات `ci.yml`

- `pip install frappe-bench==5.31.1`: إصدار مثبَّت بدل "أحدث إصدار".
- `bench init --frappe-branch version-16`: بدون هذا الخيار يُستنسخ الفرع الافتراضي لـ`frappe` (`develop`)، وهو لا يتوافق مع `erpnext` `version-16`.
- `bench get-app --branch version-16 --skip-assets <name> <url>` لـ`payments` ثم `erpnext` ثم `webshop`، بروابط صريحة.
- `install-app` لكل تطبيق بترتيب الاعتماديات (`dependencies`) قبل `frappe_shop`.


### الـ`commits` والرفع

```bash
git reset -q                       # إلغاء التجهيز للبدء بتجهيز كل جزء على حدة
git add specs/ && git commit -m "docs: add plan, research and tasks for book catalog (001)"
git add <core files> && git commit -m "feat: add book fields as fixtures, author filter and cash on delivery setup"
git add frappe_shop/demo && git commit -m "feat: add idempotent sample books function for demo"
git add <tests, setup/testing.py, hooks.py> && git commit -m "test: add server tests for book catalog"
git add .github/workflows/ci.yml && git commit -m "ci: install payments, erpnext and webshop on version-16"
git add docs/learning-log.md && git commit -m "docs: add learning log entry for book catalog implementation"
pre-commit run --all-files
git push -u origin feat/001-book-catalog
```

- سطر `before_tests` في `hooks.py` حُذف مؤقتاً قبل `commit` الـ`feat` ثم أُعيد في `commit` الـ`test`، حتى لا يشير أي `commit` إلى ملف غير موجود فيه.
- **ملاحظة:** في `commit` الـ`ci` ظهر `(no files to check)` حتى لـ`check yaml`. السبب أن `exclude: 'node_modules|.git'` في `.pre-commit-config.yaml` تعبير نمطي (`regex`)، و`.git` فيه يطابق `.github/` أيضاً، فملفات `CI` لا تُفحص أبداً. تحققنا من صحة الـ`YAML` يدوياً بـ`yaml.safe_load`. يمكن إصلاح الأمر لاحقاً في `PR` منفصل.
- **مخرجات الرفع:** `* [new branch] feat/001-book-catalog -> feat/001-book-catalog`، والرابط `https://github.com/jaguar-mahdi/frappe-shop/pull/new/feat/001-book-catalog`.

### الخطوات التالية

1. افتح الـ`PR` وراقب `Server`. هذه أول مرة يثبّت فيها `CI` تطبيقات `erpnext` و`webshop`، فقد يستغرق التشغيل نحو 15–25 دقيقة.
2. الإصدار `0.1.0` (`release`) خطوة منفصلة.

---

## 2026-11-21 — إصلاح `Frappe Linter` في `PR #11`

### الخطأ

```text
frappe_shop/setup/testing.py
❯❱ frappe-semgrep-rules.rules.frappe-manual-commit  ❰❰ Blocking ❱❱
34┆ frappe.db.commit()  # nosemgrep: test setup must persist before tests start
```

قرأناه بـ`gh run view <run-id> --log-failed`، وهو يعرض فقط سجلات الخطوات التي فشلت.

### الجذر

1. **صيغة `nosemgrep` خاطئة.** النص بعد `nosemgrep:` يُقرأ كقائمة معرّفات قواعد (`rule IDs`). فقرأ Semgrep جملتي التوضيحية كقاعدة غير معروفة، ولم يتجاهل القاعدة المقصودة. الصيغة الصحيحة: التوضيح في سطر تعليق مستقل، ثم `# nosemgrep: frappe-semgrep-rules.rules.frappe-manual-commit` على سطر الـ`commit`.
2. **هل نحتاج الـ`commit` أصلاً؟** لا:
   - `erpnext` `v16` لم يعد فيه `before_tests`.
   - `before_tests` الخاص بـFrappe (`frappe/utils/install.py`) ينتهي بـ`frappe.db.commit()`، لكنه يستدعي `complete_setup_wizard()` ثم يغيّر إعدادات أخرى بعده.
   - عندنا `setup_complete()` ينفّذ `frappe.db.commit()` بنفسه في آخر مراحله (`run_post_setup_complete`)، ولا نكتب شيئاً في قاعدة البيانات بعده.
   - ومشغّل الاختبارات (`frappe/testing/environment.py`) لا ينفّذ `commit` بعد الـ`hooks`، لكننا لا نحتاج ذلك.

### الحل

- حذف السطر بدل إسكات القاعدة: أفضل `nosemgrep` هو ألا تحتاجه. وضعنا مكانه تعليقاً يشرح لماذا لا يوجد `commit`.
- تحققنا على موقع جديد بلا شركة (`ci-check.localhost`): `Ran 19 tests ... OK`، والشركة `Frappe Books Test` بقيت بعد الـ`rollback`. ثم حذفنا الموقع.

```bash
git commit -m "fix: remove manual commit from before_tests"
git push
gh pr checks 11 --watch
```

- `gh pr checks <n> --watch`: ينتظر ويحدّث حالة الفحوص حتى تنتهي كلها.
## 2026-11-21 — تثبيت `gh` وقاعدة دمج الـ`PR`

### الأوامر

```bash
curl -s "https://api.github.com/repos/cli/cli/releases?per_page=6"        # قائمة الإصدارات
curl -sSLO https://github.com/cli/cli/releases/download/v2.103.3/gh_2.103.3_linux_amd64.tar.gz
curl -sSLO https://github.com/cli/cli/releases/download/v2.103.3/gh_2.103.3_checksums.txt
grep "linux_amd64.tar.gz" gh_2.103.3_checksums.txt | sha256sum -c -
tar -xzf gh_2.103.3_linux_amd64.tar.gz && install -m 0755 gh_2.103.3_linux_amd64/bin/gh ~/.local/bin/gh
gh auth login        # نفّذه المسؤول بنفسه: GitHub.com، HTTPS، متصفح
gh auth status
gh api repos/jaguar-mahdi/frappe-shop/rulesets/27508557
```

- اخترنا `v2.103.3` وليس أحدث إصدار (`v2.105.0`، عمره 3 أيام)، لأن الإصدار الذي مضى عليه وقت أقل مخاطرة. وهو مثبَّت صراحة.
- `sha256sum -c -`: يقارن بصمة الملف المنزَّل بالبصمة المنشورة. ظهر `OK`، أي أن الملف لم يتلف ولم يُعبث به.
- `install -m 0755`: ينسخ الملف ويجعله قابلاً للتنفيذ. المجلد `~/.local/bin` داخل `PATH` ولا يحتاج `sudo`.
- `gh auth status`: ظهر `Logged in ... jaguar-mahdi`، وصلاحيات الـ`token` هي `repo` و`workflow`.
- `gh api .../rulesets/<id>`: أظهر القواعد الفعلية:
  - `allowed_merge_methods: ["squash"]`.
  - `required_status_checks` تشمل الفحوص الثلاثة.
  - `strict_required_status_checks_policy: true`، أي يجب أن يكون الفرع محدَّثاً مع `main` قبل الدمج.
  - `bypass_actors: []`، أي لا أحد يتجاوز القواعد.

### القاعدة الجديدة

صار مسموحاً لـClaude أن يفتح الـ`PR` ويدمجها بـ`gh pr merge --squash` فقط بعد نجاح كل الفحوص المطلوبة، دون `--admin`، ودون `push` إلى `main`.
- `CLAUDE.md` لا يجوز أن يخالف الدستور، فعُدِّل الدستور إلى `1.1.0`.
- الرفع `MINOR` لأن التوجيه في قسم `Development Workflow` تغيّر جوهرياً دون حذف أي مبدأ أو إعادة تعريفه.

---

## 2026-11-21 — تجهيز الإصدار `0.1.0`

### ما الذي أُنجز

- `frappe_shop/__init__.py`: `__version__ = "0.1.0"`. الملف `pyproject.toml` يقرأ الإصدار منه (`dynamic = ["version"]` عبر `flit`).
- `CHANGELOG.md` بصيغة `Keep a Changelog`. بُني من `git log --format='%h %s' main`، وكل `commit` بصيغة `Conventional Commits` وُضع في قسم:
  - `feat` في `Added`.
  - `ci` و`docs` التي غيّرت طريقة العمل في `Changed`.
  - `fix` في `Fixed`.
- `docs/releasing.md`: الخطوات بالترتيب: `PR` لرفع الإصدار، ثم `merge`، ثم الوسم `vX.Y.Z`، ثم `GitHub Release`، ثم `release workflow`. وفيه جدول يربط `Conventional Commits` بـ`MAJOR`/`MINOR`/`PATCH`.

### لماذا `0.1.0`؟

- `0.x` يعني أن الواجهة غير مستقرة بعد.
- `MINOR` (`0.0.1 → 0.1.0`) لأن الفرع فيه `feat` (ميزة جديدة).

### الأوامر

```bash
git switch -c chore/release-0.1.0
sed -i 's/^__version__ = "0.0.1"$/__version__ = "0.1.0"/' frappe_shop/__init__.py
git log --format='%h %s' main
pre-commit run --all-files
gh pr create --title "chore(release): 0.1.0" ...
```

- `sed -i 's/A/B/' file`: يستبدل `A` بـ`B` داخل الملف نفسه (`-i` = `in-place`). علامتا `^` و`$` تضمنان مطابقة السطر كاملاً فقط.
- عنوان الـ`PR` هو `chore(release): 0.1.0`. الجزء `(release)` هو `scope` في `Conventional Commits`.

---

## 2026-11-21 — `release workflow`: صورة `Docker` على `GHCR` ونشر (`deployment`) إلى `staging`

### القرارات ومصادرها

- **قرأنا توثيق `frappe_docker` الحالي** (`docs/02-setup/02-build-setup.md`) و`README` الخاص بـ`docker/*` بدل الاعتماد على الذاكرة:
  - الطريقة الموثَّقة هي `images/layered/Containerfile` مع `--build-arg=FRAPPE_BRANCH=version-16`.
  - يُمرَّر `apps.json` كـ`BuildKit secret` باسم `apps_json`. التوثيق يحذّر من `--build-arg` لأنه يظهر دائماً في `docker image history`.
  - **لا يوجد `APPS_JSON_BASE64` في التوثيق الحالي**، فهو من طريقة قديمة.
- **`frappe_docker` مثبَّت على `v4.2.0`** (الـ`commit` `61d35da`، عمره نحو 3 أسابيع)، وليس `#main`. سياق البناء (`context`) هو `https://github.com/frappe/frappe_docker.git#<sha>`.
- **`apps.json`** يُكتب أثناء التشغيل (`heredoc`):
  - `payments` و`erpnext` و`webshop` على `version-16`.
  - `frappe_shop` على وسم الإصدار (`github.event.release.tag_name`). الحقل `branch` يقبل الوسم، لأن `git clone --branch` يقبل الوسوم.
- **الوسوم (`tags`)** عبر `docker/metadata-action`:
  - `type=semver,pattern={{version}}` تعطي `0.1.0`.
  - `type=sha,format=long` تعطي `sha-<40 حرفاً>`.
  - `flavor: latest=false` يمنع `latest`.
- **كل `action` مثبَّتة على `SHA` كامل من 40 حرفاً** مع تعليق الإصدار. الوسم مثل `v7` يمكن تحريكه، أما الـ`SHA` فلا يتغيّر.
- `permissions: contents: read, packages: write`، والمصادقة بـ`GITHUB_TOKEN` فقط، أي لا أسرار دائمة.
- `environment: staging` مع `url`: GitHub يسجّل `deployment` تلقائياً لأي `job` يحمل `environment`.

### ملاحظات

- طلبتُ تثبيت `actionlint` لفحص الـ`workflow`، فرفضه نظام الصلاحيات. تحققنا من صحة الـ`YAML` بـ`yaml.safe_load` فقط.
- `pre-commit` لا يفحص `.github/` بسبب `exclude: 'node_modules|.git'`.
- هذا الـ`workflow` لا يعمل داخل `PR`، بل عند نشر الإصدار فقط. لذلك يُختبر فعلياً في الخطوة التالية (`gh release create`).

---

## 2026-11-21 — إصدار `v0.1.0`: `GitHub Release` ثم صورة `GHCR` ثم `deployment` إلى `staging`

### الأوامر ومعنى مخرجاتها

```bash
gh pr merge 14 --squash --delete-branch
git switch main && git pull --ff-only origin main
gh release create v0.1.0 --target main --generate-notes --title "v0.1.0"
gh run list --workflow release.yml --limit 1
gh run watch 44905058807 --exit-status
gh api repos/jaguar-mahdi/frappe-shop/deployments
gh api repos/jaguar-mahdi/frappe-shop/deployments/<id>/statuses
gh api repos/jaguar-mahdi/frappe-shop/environments
```

- `gh release create`:
  - أنشأ الوسم `v0.1.0` على `main` (`dcc2d11`)، والإصدار `https://github.com/jaguar-mahdi/frappe-shop/releases/tag/v0.1.0`.
  - `--generate-notes` كتب قائمة الـ`PRs`.
  - الإصدار أُنشئ بـ`token` المستخدم (`gh`) لا بـ`GITHUB_TOKEN`، ولذلك أطلق حدث `release: published`. الأحداث التي ينشئها `GITHUB_TOKEN` لا تُطلق `workflows` أخرى.
- `gh run watch --exit-status`: ينتظر التشغيل ويعيد رمز خروج غير صفري إذا فشل. **النتيجة:** `success` في نحو 7 دقائق.
- سجل البناء أكّد التطبيقات: `payments==16.0.1` و`erpnext==16.60.0` و`webshop==0.0.1` و`frappe-shop==0.1.0`. البناء سريع لأن `layered` يبدأ من الصورتين الجاهزتين `frappe/build` و`frappe/base`.
- `deployments`: `environment: staging` و`ref: v0.1.0` و`state: success`. أنشأ GitHub البيئة `staging` تلقائياً وبلا قواعد حماية (`protection_rules: 0`).

### خطأ: `HTTP 403` عند فحص الحزمة

```text
gh: You need at least read:packages scope to get a package. (HTTP 403)
```

- **الجذر:** صلاحيات `token` الخاص بـ`gh` هي `repo` و`workflow` و`gist` و`read:org`، وليس بينها `read:packages`.
- **الحل البديل دون تسجيل دخول جديد:** سجل البناء، ثم `Registry API` مباشرة:

```bash
T=$(curl -s "https://ghcr.io/token?scope=repository:jaguar-mahdi/frappe-shop:pull" | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $T" -H 'Accept: application/vnd.oci.image.index.v1+json' https://ghcr.io/v2/jaguar-mahdi/frappe-shop/manifests/0.1.0
```

  - النتائج: `0.1.0` أعاد `200`، و`sha-dcc2d11e…` أعاد `200`، و`latest` أعاد `404`، وهذا مقصود.
  - الـ`token` هنا مجهول (`anonymous`)، فنجاح السحب يعني أن الحزمة حالياً قابلة للسحب علناً. ما زال هذا قراراً مفتوحاً للمسؤول.
  - لفحصها بـ`gh api` لاحقاً: `gh auth refresh -s read:packages`.

### قرارات مفتوحة للمسؤول

1. ظهور الحزمة (`visibility`): الحالة الآن قابلة للسحب العلني، وتُغيَّر من صفحة الحزمة ← `Package settings`.
2. موافقة يدوية (`required reviewers`) على `staging`: الآن لا توجد، وتُضاف من `Settings` ← `Environments` ← `staging`.

---

## 2026-11-21 — سدّ ثغرة `pre-commit` في `.github/`

### الخطأ

`exclude: 'node_modules|.git'` تعبير نمطي (`regex`) يُطابَق بـ`re.search` على مسار كل ملف:
- النقطة `.` تعني أي حرف.
- لا يوجد `/` يحدد بداية اسم المجلد ونهايته.

لذلك طابق النمط `.github/workflows/ci.yml` و`.gitignore`، فاستُبعدت ملفات `CI` من كل الخطافات بصمت.

### الحل

```yaml
exclude: '(^|/)(\.git|node_modules)/'
```

- `(^|/)`: بداية المسار أو بعد `/`، أي اسم مجلد كامل.
- `\.git`: نقطة حقيقية، وليس أي حرف.
- `/` في النهاية: المجلد نفسه فقط، لا `.github` ولا `.gitignore`.

### التحقق

```bash
git stash && pre-commit run check-yaml --files .github/workflows/ci.yml   # (no files to check)Skipped
git stash pop && pre-commit run check-yaml --files .github/workflows/ci.yml   # Passed
pre-commit run --all-files                                                    # exit=0
```

- `git stash` يحفظ التعديل مؤقتاً ويعيد الملف إلى حالته الأصلية، و`git stash pop` يعيد التعديل. بهذا قارنّا النمطين على الملف نفسه.
- لم يظهر أي خطأ جديد في `.github/`: الخطافات المنطبقة هناك هي `check-yaml` و`check-merge-conflict`، ونجحت كلها.
## 2026-11-21 — `CodeQL`: تفعيل `default setup` وإصلاح التنبيه #1

### الأوامر

```bash
gh api repos/jaguar-mahdi/frappe-shop/code-scanning/default-setup                 # state: not-configured
gh api -X PATCH repos/jaguar-mahdi/frappe-shop/code-scanning/default-setup -f state=configured -f query_suite=default
gh run watch <run-id>
gh api "repos/jaguar-mahdi/frappe-shop/code-scanning/alerts?state=open"
```

- `-X PATCH`: يعدّل إعداداً موجوداً. `-f key=value` يرسل حقلاً في جسم الطلب (`body`).
- الـ`token` كان كافياً: لديه صلاحية `repo`، والمستخدم هو المالك.

### خطأ ظهر في أول تحليل: `Analyze (javascript-typescript)` فشل

```text
Only found JavaScript or TypeScript files that were empty or contained syntax errors.
CodeQL detected code written in JavaScript/TypeScript but could not process any of it.
```

- **الجذر:** ملف JS الوحيد في التطبيق هو `book_author.js`، وهو قالب مولَّد تلقائياً وشبه فارغ، فلم يجد `CodeQL` شيئاً يحلّله.
- **الحل:** لا يحتاج شيئاً. الـ`job` المسمى `Adjust Configuration` حذف `javascript-typescript` من اللغات تلقائياً، فصارت `["actions", "python"]`، وأصبحت نتيجة التشغيل كله `success`.

### التنبيه #1: `actions/missing-workflow-permissions` (`medium`) في `.github/workflows/ci.yml`

- **حقيقي:** `ci.yml` بلا كتلة `permissions`، فيأخذ `GITHUB_TOKEN` الصلاحيات الافتراضية للمستودع، وقد تكون كتابة. هذا مخالف لمبدأ أقل صلاحية (`least privilege`).
- **الحل:** `permissions: contents: read` في أعلى الملف. الـ`job` `Server` يقرأ الكود فقط. أما `linter.yml` و`release.yml` ففيهما الكتلة أصلاً.
- `Dependabot alerts` و`secret scanning alerts`: صفر تنبيهات مفتوحة.

---

## 2026-11-21 — إصلاح: `Place Order` يتجمّد في المتجر

### العَرَض

العميل يضغط `Place Order` على `http://development.localhost:8001` فتبقى الصفحة مجمَّدة بلا رسالة.

### الأدلة، بالترتيب

| الأمر أو الأداة | النتيجة |
|---|---|
| `bench --site development.localhost show-pending-jobs` | لا مهام معلّقة |
| `Error Log` | لا شيء متعلق بالطلب (فقط رسالة `dashboard` لا علاقة لها) |
| `curl ... /api/method/webshop.webshop.shopping_cart.cart.place_order` بمستخدم موقع (`Website User`) تجريبي | `HTTP 500` بصيغة `HTML` من `Werkzeug`: `BrokenPipeError: [Errno 32] Broken pipe` |
| استخراج إطارات الـ`traceback` من الصفحة | `cart.py:133` (`throw`)، ثم `handle_exception`، ثم `report_error`، ثم `frappe.errprint`، ثم `print(msg)` الذي فشل |
| `ls -l /proc/<pid>/fd/1` و`ps -o ppid` | `stdout` الخاص بـ`web.1` هو `pipe`، والأب `ppid 1`، و`honcho` في حالة `<defunct>` منذ `11:18` |
| خادم مؤقت سليم `bench serve --port 8011` | الطلب نفسه أعاد `HTTP 500 application/json` بـ`QueryTimeoutError` بعد 50 ثانية بالضبط |
| `information_schema.innodb_trx` (بـ`root`، قراءة فقط) | معاملة `RUNNING`/`Sleep` تحمل قفلاً (`rows_locked 1`)، واتصالها (`ss -tnp`) يخص عملية `web.1` القديمة |
| `request.js` و`cart.js` | عند `500` يُستدعى `error_callback` فقط، و`cart.js` يمرر `callback` فقط، فلا يُستدعى `unfreeze()` أبداً |

### السبب الجذري

1. **البيئة:** مدير العمليات `honcho` (`bench start`) مات، فبقي `web.1` يتيماً و`stdout` فيه أنبوب لا يقرؤه أحد.
2. أي خطأ في `place_order` يمر عبر `report_error` ثم `print()`، فيقع `BrokenPipeError` **داخل معالج الأخطاء نفسه، قبل الـ`rollback`**. تبقى المعاملة مفتوحة وتحتفظ بالقفل، ولا يُكتب شيء في `Error Log`.
3. كل `Place Order` بعدها ينتظر القفل 50 ثانية (`innodb_lock_wait_timeout`) ثم يفشل بـ`QueryTimeoutError`. المتصفح يستلم `HTML 500`، و`cart.js` لا يفك التجميد، فيبدو الأمر تعليقاً.
4. **خطأ إعدادات حقيقي يظهر حتى على خادم سليم:** `Portal Settings.default_role` فارغ. المستخدمون الجدد ليس لديهم دور `Customer`، فرسالة `Please add Customer role to user` تظهر، وصفحة تأكيد الطلب `/orders/<name>` تعيد `HTTP 403 Not Permitted` بعد نجاح الطلب. تحققنا بإضافة الدور: `403` صارت `200`.

### الحل

- **البيئة:** أعاد المسؤول تشغيل `bench start` بعد إيقاف العمليات القديمة بأرقامها (`kill <pid>`):
  - رفض نظام الصلاحيات أن أوقف عمليات طرفية المستخدم بنفسي، وهذا صحيح.
  - المحاولة الأولى فشلت بـ`EADDRINUSE :::9001` لأن `socketio` القديم كان ما يزال يحجز المنفذ.
  - تحققنا بعدها: `honcho` جديد، و`pipe` جديد، و`open trx: 0`.
- **الإعدادات (في `frappe_shop` فقط):** `setup_store` يضبط الآن `Portal Settings.default_role = "Customer"` إن كان فارغاً، ولا يغيّر قيمة اختارها المالك.
  - هذا ما يتوقعه `erpnext`: الـ`hook` `create_customer_or_supplier` عند الدخول يعتمد على الدور الافتراضي.
  - لم نغيّر `disable_signup`، لأن السماح بالتسجيل العام قرار منتج.

### التحقق

- بعد إعادة التشغيل: `place_order` بلا عنوان أعاد `HTTP 417 application/json` في 0.2 ثانية برسالة واضحة، ولا تجميد.
- مع عنوان: `HTTP 200` (`SAL-ORD-2026-00002`)، وصفحة الطلب `HTTP 200` بلا زر `Pay`، و`open trx: 0`.
- اختبار انحدار (`regression test`) اسمه `test_new_website_users_get_customer_role`، يمر عبر `sign_up` الحقيقي. يفشل بدون الإصلاح (`'' != 'Customer'`) وينجح معه. إجمالي الاختبارات: `Ran 21 tests ... OK`.

### خطأ أثناء الاختبار

- `ValidationError: Sign Up is disabled`: الموقع يمنع التسجيل العام. الحل: داخل الاختبار فقط نضبط `disable_signup = 0` ونعيده بـ`addCleanup`.

### دروس

- `pkill -f "<pattern>"` قد يطابق سطر أوامر الـ`shell` نفسه فيقتله (رمز الخروج `144`). الأفضل `kill <pid>` بعد التحقق.
- `HTTP 500` بصيغة `HTML` بدل `JSON` في `API` إشارة إلى أن معالج الأخطاء نفسه فشل.
