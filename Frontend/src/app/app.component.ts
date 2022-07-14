import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from 'rxjs';
import {ApiService} from 'src/model/api.service';
import {GroupRank, MatchResult, TeamInfo} from 'src/model/model';
import {ToastrService} from 'ngx-toastr';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit, OnDestroy {
  constructor(private apiService: ApiService, private toast: ToastrService) { }

  title: string = 'Frontend';

  infoField: string = '';
  teamInfoSubs: Subscription = Subscription.EMPTY;
  teamInfoArr: TeamInfo[] = [];

  resultField: string = '';
  matchResultSubs: Subscription = Subscription.EMPTY;
  matchResultArr: MatchResult[] = [];

  rankingSubs: Subscription = Subscription.EMPTY;
  rankingArr: GroupRank[] = [];

  ngOnInit() {
    this.updateTeamInfo();
    this.updateMatchResult();
  }

  ngOnDestroy() {
    this.teamInfoSubs.unsubscribe();
    this.matchResultSubs.unsubscribe();
    this.rankingSubs.unsubscribe();
  }


  changeInfoField(event: any) {
    if (!(event.target.value as string)) return;
    this.infoField = event.target.value as string;
  }

  onClickInfo() {
    if (!this.infoField) {
      this.toast.error('Text Field Cannot Be Empty');
      return;
    }
    this.teamInfoSubs = this.apiService
        .addTeamInfo(this.infoField)
        .subscribe((res) => {
          this.updateTeamInfo();
          this.toast.success('Team Information Saved');
        },
        (err) => {
          this.toast.error('Failed: ' + err.error);
        },
        );
  }

  changeResultField(event: any) {
    if (!(event.target.value as string)) return;
    this.resultField = event.target.value as string;
  }

  onClickResult() {
    if (!this.resultField) {
      this.toast.error('Text Field Cannot Be Empty');
      return;
    }
    this.matchResultSubs = this.apiService
        .addMatchResult(this.resultField)
        .subscribe((res) => {
          this.toast.success('Match Results Saved');
          this.updateMatchResult();
        },
        (err) => {
          this.toast.error('Failed: ' + err.error);
        },
        );
  }

  onClickDeleteDb() {
    this.apiService.deleteAll()
        .subscribe(() => {
          this.teamInfoArr = [];
          this.matchResultArr = [];
          this.rankingArr = [];
          this.toast.success('Database Cleared');
        },
        (error) => {
          this.toast.error('Database Not Cleared');
        },
        );
  }

  updateTeamInfo() {
    this.teamInfoSubs = this.apiService
        .getTeamInfo()
        .subscribe((res) => {
          this.castToTeamInfo(res);
          this.toast.success('Team Information Loaded');
          this.updateRanking();
        } );
  }

  updateMatchResult() {
    this.matchResultSubs = this.apiService
        .getMatchResult()
        .subscribe((res) => {
          this.castToMatchResult(res);
          this.toast.success('Match Result Loaded');
          this.updateRanking();
        } );
  }

  updateRanking() {
    if (!this.matchResultArr.length || !this.teamInfoArr.length) return;

    this.rankingSubs = this.apiService
        .getRanking()
        .subscribe((res) => {
          this.castToGroupRank(res);
          this.toast.success('Ranking Calculated');
        },
        (error) => {
          this.toast.error('Error Calculating Ranking');
        },
        );
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
    this.rankingArr = temp;
  }
}
