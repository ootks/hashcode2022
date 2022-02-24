file = "a.txt"
contributors = dict()
skills = set()
projects = dict()
project_skills = dict()
with open(file) as f:
    ncontributors, nprojects = [int(x) for x in f.readline().split(" ")]
    # Get each contributor and the skills they have
    for i in range(ncontributors):
        name, nskills = f.readline().split(" ")
        nskills = int(nskills)
        contributors[name] = {}
        for j in range(nskills):
            skill, level = f.readline().split(" ")
            level = int(level)
            contributors[name][skill] = level
            skills.add(skill)
    # backfill the skills that weren't listed for each contributor
    for contributor in contributors:
        for skill in skills:
            if skill not in contributors[contributor]:
                contributors[contributor][skill] = 0
    # Parse the project information
    for i in range(nprojects):
        name, days, score, bestby, nroles = f.readline().split(" ")
        days = int(days)
        score = int(score)
        bestby = int(bestby)
        nroles = int(nroles)
        projects[name] = (days, score, bestby, nroles)
        project_skills[name] = dict()
        for i in range(nroles):
            skill, level = f.readline().split(" ")
            project_skills[name][skill] = int(level)
print(contributors)
print(skills)
print(projects)
print(project_skills)
