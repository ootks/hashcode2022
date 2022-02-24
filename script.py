filename = "c.txt"
contributors = dict()
skills = set()
projects = dict()
project_skills = dict()
final_deadline = -1
with open(filename) as f:
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
    # backfill the skills that weren't listed for bach contributor
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
        final_deadline = max(final_deadline, bestby + score)
        projects[name] = (days, score, bestby, nroles)
        project_skills[name] = list()
        for i in range(nroles):
            skill, level = f.readline().split(" ")
            project_skills[name].append((skill, int(level)))

def is_possible(project_roles, available_workers):
    workers = list(available_workers)
    adj = [[1 if can_work(worker, role) else 0 for role in project_roles] for worker in workers]
    g = GFG(adj)
    n, assignment = g.maxBPM()
    if n < len(project_roles):
        return False, []
    return True, [workers[i] for i in assignment]


def can_work(worker, role):
    return contributors[worker][role[0]] >= role[1]


class GFG:
    def __init__(self,graph):
         
        # residual graph
        self.graph = graph
        self.ppl = len(graph)
        self.jobs = len(graph[0])
 
    # A DFS based recursive function
    # that returns true if a matching
    # for vertex u is possible
    def bpm(self, u, matchR, seen):
 
        # Try every job one by one
        for v in range(self.jobs):
 
            # If applicant u is interested
            # in job v and v is not seen
            if self.graph[u][v] and seen[v] == False:
                 
                # Mark v as visited
                seen[v] = True
 
                '''If job 'v' is not assigned to
                   an applicant OR previously assigned
                   applicant for job v (which is matchR[v])
                   has an alternate job available.
                   Since v is marked as visited in the
                   above line, matchR[v]  in the following
                   recursive call will not get job 'v' again'''
                if matchR[v] == -1 or self.bpm(matchR[v],
                                               matchR, seen):
                    matchR[v] = u
                    return True
        return False
 
    # Returns maximum number of matching
    def maxBPM(self):
        '''An array to keep track of the
           applicants assigned to jobs.
           The value of matchR[i] is the
           applicant number assigned to job i,
           the value -1 indicates nobody is assigned.'''
        matchR = [-1] * self.jobs
         
        # Count of jobs assigned to applicants
        result = 0
        for i in range(self.ppl):
             
            # Mark all jobs as not seen for next applicant.
            seen = [False] * self.jobs
             
            # Find if the applicant 'u' can get a job
            if self.bpm(i, matchR, seen):
                result += 1
        return result, matchR
 
# This code is contributed by Neelam Yadav
output = open("out."+filename, "w")
all_coders = contributors.keys()
earliest_available = {coder: 0 for coder in all_coders}
print("made_coders_available")
completed_days = dict()
n_projects = 0
final_deadline = 5000
for day in range(final_deadline+1):
    available_coders = [coder for coder in all_coders if earliest_available[coder] >= day]
    if len(projects) == 0:
        break
    print("{} out of {}".format(day, final_deadline))
    # Find the best project at each day
    best_score = -1
    best_project = ""
    best_workers_needed = []
    if len(projects) == 0:
        break
    for project in projects:
        # determine if the project is possible, and if so, which workers are needed
        project_possible, workers_needed = is_possible(project_skills[project], available_coders)
        days_needed, score, bestby, nroles = projects[project]
        if project_possible:
            # score project
            penalty = min(max(bestby - day - days_needed, -score), 0)
            value = (score + penalty)/days_needed
            if value == 0:
                continue
            if value > best_score:
                best_score = score
                best_project = project
                best_workers_needed = workers_needed
    if best_project == "":
        continue
    n_projects += 1
    print(best_project)
    output.write(best_project + "\n")
    output.write(" ".join(best_workers_needed) + "\n")
    days_needed, score, bestby, nroles = projects[best_project]
    # Make the workers unavailable for the days of the project.
    for worker in best_workers_needed:
        earliest_available[worker] = day + days_needed
    completion_date = day + days_needed
    if completion_date not in completed_days:
        completed_days[completion_date] = []
    completed_days[completion_date].append((best_project, best_workers_needed))
    del projects[best_project]
    # update worker skills
    if day in completed_days:
        for project, workers in completed_days[day]:
            for worker, role in zip(workers, project_skills[project]):
                if contributors[worker][role[0]] <= role[1]:
                    contributors[worker][role[0]] += 1
print(n_projects)