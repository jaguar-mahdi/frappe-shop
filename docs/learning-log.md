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
