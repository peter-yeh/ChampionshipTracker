import {Component} from '@angular/core';
import {Subscription} from 'rxjs';
import {ApiService} from 'src/model/api.service';
import {MatchResult, TeamInfo} from 'src/model/model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  constructor(private apiService: ApiService) { }

  title: string = 'Frontend';

  inputStringInfoField: string = ``;
  teamInfoSubs: Subscription = Subscription.EMPTY;
  teamInformationArr: TeamInfo[] = [];

  inputStringResultField: string = ``;
  matchResultSubs: Subscription = Subscription.EMPTY;
  matchResultArr: MatchResult[] = [];

  onInputChangeInfoField(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.inputStringInfoField = event.target.value as string;
  }

  onClickInfoBtn() {
    if (!this.inputStringInfoField) {
      // can show toast message if no input
      return;
    }
    this.teamInfoSubs = this.apiService
        .addTeamInfo(this.inputStringInfoField)
        .subscribe((res) => {
          this.castToTeamInfo(res);
        },
        console.error,
        );
    // show toast message for success
  }

  onInputChangeResultField(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.inputStringResultField = event.target.value as string;
  }

  onClickResultBtn() {
    if (!this.inputStringResultField) {
      // can show toast message if no input
      return;
    }
    this.matchResultSubs = this.apiService
        .addMatchResult(this.inputStringResultField)
        .subscribe((res) => {
          this.castToTeamInfo(res);
        },
        console.error,
        );
    // show toast message for success
  }

  castToTeamInfo(anyArr: any[]) {
    const temp = [];
    for (let i = 0; i < anyArr.length; i++) {
      const teamInfo: TeamInfo = new TeamInfo(anyArr[i][0], anyArr[i][1], anyArr[i][2]);
      temp.push(teamInfo);
    }
    this.teamInformationArr = temp;
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
}
