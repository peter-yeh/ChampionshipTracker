import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { ApiService } from 'src/model/api.service';
import { TeamInfo } from 'src/model/model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private apiService: ApiService) { }

  title: string = 'Frontend';
  inputString: string = '';

  teamInfoSubs: Subscription = Subscription.EMPTY
  teamInformationArr: TeamInfo[] = [];



  onInputChange(event: any) {
    if (!(event.target.value as string)) {
      // show toast message if no input
      return;
    }
    this.inputString = event.target.value as string;
  }

  onClick() {
    if (!this.inputString) {
      // can show toast message if no input
      return;
    }
    this.teamInfoSubs = this.apiService
      .addTeamInfo(this.inputString)
      .subscribe(res => {
        this.teamInformationArr = res;
      },
        console.error
      );
    // show toast message for success
  }

}
