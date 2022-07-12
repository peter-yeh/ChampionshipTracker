export class TeamInfo {
  constructor(
  public name: string,
  public regDate: Date,
  public groupNumber: number,
  ) { }
}

export class MatchResult {
  constructor(
    public teamA: string,
    public scoreA: number,
    public teamB: string,
    public scoreB: number,
  ) { }
}

export class GroupRank {
  constructor(
    public name: string,
    public rank: any[],
  ) { }
}
