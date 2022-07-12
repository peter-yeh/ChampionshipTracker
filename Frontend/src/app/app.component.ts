import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs';
import {ApiService} from 'src/model/api.service';
import {GroupRank, MatchResult, TeamInfo} from 'src/model/model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit, OnDestroy {
  constructor(private apiService: ApiService) { }

  title: string = 'Frontend';

  infoField: string = ``;
  teamInfoSubs: Subscription = Subscription.EMPTY;
  teamInfoArr: TeamInfo[] = [];

  resultField: string = ``;
  matchResultSubs: Subscription = Subscription.EMPTY;
  matchResultArr: MatchResult[] = [];

  rankingSubs: Subscription = Subscription.EMPTY;
  groupRankArr: GroupRank[] = [];

  ngOnInit() {
    this.teamInfoSubs = this.apiService
        .getTeamInfo()
        .subscribe((res) => {
          this.castToTeamInfo(res);
        },
        console.error,
        );
    this.matchResultSubs = this.apiService
        .getMatchResult()
        .subscribe((res) => {
          this.castToMatchResult(res);
        },
        console.error,
        );
    this.rankingSubs = this.apiService
        .getRanking()
        .subscribe((res) => {
          this.castToGroupRank(res);
          console.log(this.groupRankArr);
        },
        console.error,
        );
  }

  ngOnDestroy() {
    this.teamInfoSubs.unsubscribe();
    this.matchResultSubs.unsubscribe();
    this.rankingSubs.unsubscribe();
  }


  changeInfoField(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.infoField = event.target.value as string;
  }

  onClickInfo() {
    if (!this.infoField) {
      // can show toast message if no input
      return;
    }
    this.teamInfoSubs = this.apiService
        .addTeamInfo(this.infoField)
        .subscribe((res) => {
          this.castToTeamInfo(res);
        },
        console.error,
        );
    // show toast message for success
  }

  changeResultField(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.resultField = event.target.value as string;
  }

  onClickResult() {
    if (!this.resultField) {
      // can show toast message if no input
      return;
    }
    this.matchResultSubs = this.apiService
        .addMatchResult(this.resultField)
        .subscribe((res) => {
          this.castToTeamInfo(res);
        },
        console.error,
        );
    // show toast message for success
  }

  onClickClearDb() {

  }

  castToTeamInfo(anyArr: any[]) {
    const temp = [];
    for (let i = 0; i < anyArr.length; i++) {
      const teamInfo: TeamInfo = new TeamInfo(anyArr[i][0], anyArr[i][1], anyArr[i][2]);
      temp.push(teamInfo);
    }
    this.teamInfoArr = temp;
  }

  castToMatchResult(anyArr: any[]) {
    const temp = [];
    for (let i = 0; i < anyArr.length; i++) {
      const matchResult: MatchResult = new MatchResult(
          anyArr[i][0], anyArr[i][1], anyArr[i][2], anyArr[i][3]);
      temp.push(matchResult);
    }
    this.matchResultArr = temp;
  }

  castToGroupRank(anyArr: any[]) {
    const temp = [];
    for (const [key, value] of Object.entries(anyArr)) {
      const rank = new GroupRank(key, value);
      temp.push(rank);
    }
    this.groupRankArr = temp;
  }
}
