from argparse import ArgumentParser, Namespace
from typing import List, Dict, Set, Tuple, Union


def main() -> None:
    result: List[str] = []
    _ = int(input())
    Parent.all_skills = set(input().split())
    n = int(input())
    parser: ArgumentParser = input_parser()
    for _ in range(n):
        try:
            args: Namespace = parser.parse_args(input().split())
            result.append(args.func(args))
        except MyValueError as e:
            result.append(str(e))

    list(map(print, result))


class MyValueError(Exception):
    pass


class Parent:
    name: str
    age: int
    min_age: int
    max_age: int
    timetype: str
    salary: int
    id: int
    skills: Dict[str, int]
    view_count: int
    id_counter: int
    members: List[Union["Job", "User", "Parent"]]

    all_skills: Set[str] = set()

    @classmethod
    def add(cls, args: Namespace) -> str:
        obj: Union["Job", "User", "Parent"] = cls()
        for arg, value in vars(args).items():
            setattr(obj, arg, value)
        obj.id = cls.id_counter
        obj.skills = {}
        obj.view_count = 0
        cls.id_counter += 1
        cls.members.append(obj)
        return f"{cls.__name__.lower()} id is {obj.id}"

    @classmethod
    def add_skill(cls, args: Namespace) -> str:
        id: int = int(args.id)
        skill: str = args.skill
        obj: "Parent" = cls.members[id - 1]
        if skill in obj.skills:
            raise MyValueError("repeated skill")
        obj.skills[skill] = 0
        return "skill added"

    @staticmethod
    def valid_skill(value: str) -> str:
        if value not in Parent.all_skills:
            raise MyValueError("invalid skill")
        return value

    @staticmethod
    def valid_name(value: str) -> str:
        if value.isalpha() and 1 <= len(value) <= 10:
            return value
        raise MyValueError("invalid name")

    @staticmethod
    def valid_age(value: str) -> int:
        age = int(value)
        if 0 <= age <= 200:
            return age
        raise MyValueError("invalid age")

    @staticmethod
    def valid_time(value: str) -> str:
        if value in {"FULLTIME", "PARTTIME", "PROJECT"}:
            return value
        raise MyValueError("invalid timetype")

    @staticmethod
    def valid_salary(value: str) -> int:
        salary = int(value)
        if salary % 1000 == 0 and 0 <= salary < 10**9:
            return salary
        raise MyValueError("invalid salary")

    @classmethod
    def valid_id(cls, value: str) -> int:
        id: int = int(value)
        if id > len(cls.members) or id <= 0:
            raise MyValueError("invalid index")
        return id


class Job(Parent):

    id_counter: int = 1
    members = []
    _min_age: int

    @classmethod
    def status(cls, args: Namespace) -> str:
        id: int = args.id
        job: "Parent" = cls.members[id - 1]
        sorted_skills: List[Tuple[str, int]] = sorted(
            job.skills.items(), key=lambda x: (x[1], x[0])
        )
        sorted_skills_str: List[str] = list(
            map(lambda x: f"({x[0]},{x[1]})", sorted_skills)
        )

        return f"{job.name}-{job.view_count}-{''.join(sorted_skills_str)}"

    @classmethod
    def valid_min_age(cls, value: str) -> int:
        age = int(value)
        if 0 <= age <= 200:
            cls._min_age = age
            return age
        raise MyValueError("invalid age interval")

    @classmethod
    def valid_max_age(cls, value: str) -> int:
        age = int(value)
        if 0 <= age <= 200 and cls._min_age <= age:
            return age
        raise MyValueError("invalid age interval")


class User(Parent):

    id_counter: int = 1
    members = []

    @classmethod
    def status(cls, args: Namespace) -> str:
        id: int = args.id
        user: "Parent" = cls.members[id - 1]
        sorted_skills: List[Tuple[str, int]] = sorted(
            user.skills.items(), key=lambda x: (x[1], x[0])
        )
        sorted_skills_str: List[str] = list(
            map(lambda x: f"({x[0]},{x[1]})", sorted_skills)
        )
        return f"{user.name}-{''.join(sorted_skills_str)}"


def view(args: Namespace) -> str:
    user_id = args.user_id
    job_id = args.job_id

    user: User = User.members[user_id - 1]
    job: Job = Job.members[job_id - 1]

    job.view_count += 1
    for skill in job.skills:
        if skill in user.skills:
            job.skills[skill] += 1
            user.skills[skill] += 1
    return "tracked"


def get_job_list(args: Namespace) -> str:
    id: int = args.id
    user: Parent = User.members[id - 1]
    user_skills: set = set(user.skills.keys())
    points: List[Tuple[int, int]] = []
    for job in Job.members:
        point: int = 0
        point += min(user.age - job.min_age, job.max_age - user.age, key=abs)
        job_skills: set = set(job.skills.keys())
        point += 3 * len(job_skills.intersection(user_skills)) - len(
            job_skills - user_skills
        )
        if job.timetype == user.timetype:
            point += 10
        elif job.timetype == "PARTTIME" or user.timetype == "PARTTIME":
            point += 5
        else:
            point += 4
        point += 1000 // max(abs(user.salary - job.salary), 1)

        point = point * 1000 + job.id

        points.append((job.id, point))

    points.sort(key=lambda x: x[1], reverse=True)
    result = [f"({i[0]},{i[1]})" for i in points[:5]]
    return "".join(result)


def input_parser() -> ArgumentParser:

    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    add_job_parser: ArgumentParser = subparsers.add_parser("ADD-JOB")
    add_job_parser.add_argument("name", type=Job.valid_name)
    add_job_parser.add_argument("min_age", type=Job.valid_min_age)
    add_job_parser.add_argument("max_age", type=Job.valid_max_age)
    add_job_parser.add_argument("timetype", type=Job.valid_time)
    add_job_parser.add_argument("salary", type=Job.valid_salary)
    add_job_parser.set_defaults(func=Job.add)

    add_user_parser: ArgumentParser = subparsers.add_parser("ADD-USER")
    add_user_parser.add_argument("name", type=User.valid_name)
    add_user_parser.add_argument("age", type=User.valid_age)
    add_user_parser.add_argument("timetype", type=User.valid_time)
    add_user_parser.add_argument("salary", type=User.valid_salary)
    add_user_parser.set_defaults(func=User.add)

    add_job_skill_parser: ArgumentParser = subparsers.add_parser("ADD-JOB-SKILL")
    add_job_skill_parser.add_argument("id", type=Job.valid_id)
    add_job_skill_parser.add_argument("skill", type=Job.valid_skill)
    add_job_skill_parser.set_defaults(func=Job.add_skill)

    add_user_skill_parser: ArgumentParser = subparsers.add_parser("ADD-USER-SKILL")
    add_user_skill_parser.add_argument("id", type=User.valid_id)
    add_user_skill_parser.add_argument("skill", type=User.valid_skill)
    add_user_skill_parser.set_defaults(func=User.add_skill)

    view_parser: ArgumentParser = subparsers.add_parser("VIEW")
    view_parser.add_argument("user_id", type=User.valid_id)
    view_parser.add_argument("job_id", type=Job.valid_id)
    view_parser.set_defaults(func=view)

    job_status_parser: ArgumentParser = subparsers.add_parser("JOB-STATUS")
    job_status_parser.add_argument("id", type=Job.valid_id)
    job_status_parser.set_defaults(func=Job.status)

    user_status_parser: ArgumentParser = subparsers.add_parser("USER-STATUS")
    user_status_parser.add_argument("id", type=User.valid_id)
    user_status_parser.set_defaults(func=User.status)

    get_joblist_parser: ArgumentParser = subparsers.add_parser("GET-JOBLIST")
    get_joblist_parser.add_argument("id", type=User.valid_id)
    get_joblist_parser.set_defaults(func=get_job_list)

    return parser
if __name__ == "__main__":
    main()
