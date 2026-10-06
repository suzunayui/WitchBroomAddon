# 月あかりのほうき / Moonweave Broom

Minecraft Bedrock Edition 用の、魔女の空飛ぶほうきアドオンです。金色の穂、曲がった木の柄、紫の巻き布、小さな水色のチャームと星の粒子を付けました。

- アドオン: v0.1.0（初回プレビュー版 / prerelease）
- 対象: Windows の Minecraft Bedrock 26.52。最低エンジン指定は 26.50 相当
- Java Edition では使えません
- 実験機能 / Beta APIs: 不要の構成
- 検証状況: JSON・依存関係・TypeScript・安全補助の模擬テストは確認済み。Minecraft 本体での読み込み / 飛行テストは未実施です。最初は必ず新しいテスト用ワールドで試してください

## Windows に入れる

1. `dist/Moonweave_Broom_v0.1.0.mcaddon` をダウンロードします。GitHub からの場合、ファイルページの「Download raw file」を使ってください
2. ファイルをダブルクリックするか、「プログラムから開く」→「Minecraft」を選びます
3. 2つのパックのインポート完了を待ちます
4. 新しいテスト用ワールドを作り、「ビヘイビアーパック」→「マイパック」で「月あかりのほうき 動作パック」を有効化します
5. 「リソースパック」でも「月あかりのほうき 見た目パック」が有効なことを確認します。依存関係により自動で有効になる構成です
6. 最初はクリエイティブ、明るく平らな場所で試します。実験機能はすべてオフのままで構いません

ファイル名が `.mcaddon.zip` になった場合は、拡張子を表示して末尾の `.zip` だけを外してください。

## ほうきを手に入れる

クリエイティブの「装備」カテゴリで「月あかりのほうき」または「Moonweave Broom」を探します。

サバイバルでは、作業台で次のように並べて1本作れます。

|   |   |   |
|---|---|---|
| 空 | 空 | 棒 |
| 空 | アメジストの欠片 | 棒 |
| 小麦 | 小麦 | 小麦 |

材料: 棒2本、小麦3個、アメジストの欠片1個。欠片を入手するとレシピを解放する設定です。

確認用コマンド（チートをオンにしたワールドのみ）:

```text
/give @s witchbroom:broom 1
```

## 操作

キー名は Windows 標準配置です。変更済みなら、それぞれ「使う」「移動」「ジャンプ」「しゃがむ」に割り当てたキーを使います。

1. ほうきアイテムを手に持ち、地面に向かって右クリックして置きます
2. 空の手に持ち替え、置いたほうきを右クリックして乗ります。サドルは要りません
3. W / A / S / D で移動、マウスで向きを変えます。上下の視線も飛行方向に使います
4. Space（ジャンプ）で上昇します
5. 下を向いて W で前進すると降下します。急角度ではなく、少しずつ下を向くと扱いやすくなります
6. 移動とジャンプを離すと減速してホバリングする構成です
7. 地面の近くで Shift（しゃがむ）を押して降ります。Shift は降下専用キーではありません
8. 回収するときは、誰も乗っていないほうきに「しゃがむ＋右クリック」。アイテムが地面に戻るので拾います

F5 で三人称視点にすると、ほうきがよく見えます。

## タッチ / コントローラー

ゲーム標準の乗り物操作を使用し、Windows 専用のキー検出はしていません。

- タッチ: ほうきを狙って「ほうきに乗る」。移動スティック＋視線操作で飛行、ジャンプで上昇、下向き＋前進で降下、降りる / しゃがむ操作で下車
- コントローラー: 「使う」で乗り、左スティック＋右スティックで飛行、ジャンプで上昇、下向き＋前進で降下、しゃがむ操作で下車
- 回収も、下車してしゃがんだ状態で「ほうきをしまう」/「使う」です

Android・iOS などでも同じ仕組みを使う設計ですが、端末ごとの実機テストは未実施です。操作UIは端末と設定により異なります。

Switch / PlayStation / Xbox は `.mcaddon` を Windows と同じ方法で直接開く前提ではありません。公式に案内されている方法は、Windows側でこのアドオンを有効にしたワールドを Realms にアップロードし、コンソールからそのワールドに入る形です。Realms 契約や機種側のオンライン利用条件が必要な場合があります。このアドオンのコンソール / Realms 動作は未確認です。

## 安全・保存・マルチプレイ

- 1本につき1人乗り。複数人はそれぞれ自分のほうきを用意します
- ブロックとの衝突を有効にしており、飛行のためにプレイヤーを毎フレーム瞬間移動させません。天井や壁には低速で近づき、狭い穴へ突っ込まないでください
- 乗っている間と降りた後には、着地まで「低速落下」を短く更新する補助を入れています。高所でも一定秒数で補助を打ち切らない設計です
- 降りたほうきは重力が戻り、地面へ落ちます。ほうき自身には落下ダメージがありません
- ほうきは自然消滅しない設定です。不要なものは回収してください
- ログアウトや再読み込みの後も着地補助の印を保持し、オンライン人数に応じた1本の処理ループで管理します。死亡後のリスポーンで古い補助は終了します
- 補助は無敵化ではありません。溶岩、炎、窒息、奈落、敵の攻撃、他アドオンの干渉には注意してください
- 水中潜航、ポータル通過、建築高度を超える飛行を目的にはしていません。移動前に降りて回収するのが安全です
- 大切なワールドは先にバックアップしてください。空中でのパック無効化・削除は避けてください

## うまくいかないとき

- 見えない / 紫黒になる: リソースパックが有効か確認
- 置けない: 手元のアイテムを地面に使う。Minecraft が Bedrock 26.50 以降か確認
- 乗れるが上昇しない: ビヘイビアーパックが有効か、他の乗り物アドオンとの競合がないか確認
- 安全補助が出ない / スクリプトエラー: バージョンとパック依存を確認。実験機能を追加でオンにして直そうとせず、エラーの表示を記録
- インポート失敗: 完全なファイルが保存されているか、拡張子が `.mcaddon` か確認。Minecraftを終了してからファイルを開き直す

初回のゲーム内確認結果は未取得なので、不具合が出たら Minecraft の正確なバージョン、端末、何をした直後か、表示されたエラーが修正の手掛かりになります。

## 開発と検証

必要: Node.js、Python 3、Pillow、NumPy。Minecraft本体は別途必要です。

```sh
npm ci
python3 -m pip install -r requirements.txt
npm run build
npm test
```

`BP/` と `RP/` が配布パック、`src/main.ts` が着地補助、`tools/` が生成・検証・梱包、`tests/` がゲーム外の検証です。生成物を直接編集した場合は、生成スクリプトに変更を反映してから再ビルドしてください。

`art-preview.png` はモデルのプレビュー画像です。Minecraft内のスクリーンショットではありません。

詳しい検証範囲は `docs/VALIDATION.md`、ゲーム内の確認項目は `docs/INGAME_CHECKLIST.md` に記載しています。

## 参考にした公式資料

- [26.50 リリースノート / 安定版 Script API 2.10.0](https://feedback.minecraft.net/hc/en-us/articles/48826825649933-Minecraft-Bedrock-Edition-26-50-Changelog-Wilderness-Bound)
- [26.52 ホットフィックス](https://feedback.minecraft.net/hc/en-us/articles/49175370527501-Minecraft-Bedrock-Edition-26-52-Hotfix-Changelog)
- [Mojang の現行パック manifest](https://github.com/Mojang/bedrock-samples/blob/main/behavior_pack/manifest.json)
- [Mojang の Happy Ghast 実装](https://github.com/Mojang/bedrock-samples/blob/main/behavior_pack/entities/happy_ghast.json)
- [free_camera_controlled](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_free_camera_controlled?view=minecraft-bedrock-stable)
- [vertical_movement_action](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vertical_movement.action?view=minecraft-bedrock-stable)
- [rideable](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rideable?view=minecraft-bedrock-stable)
- [Script API Entity](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/minecraft/server/entity?view=minecraft-bedrock-stable)
- [Bedrock Add-On 導入 / Realms・コンソール](https://learn.microsoft.com/en-us/minecraft/creator/documents/gettingstarted?view=minecraft-bedrock-stable)

本アドオンは非公式のオリジナル作品です。Mojang / Microsoft の公式製品ではありません。Minecraftの画像・音声・モデルを同梱していません。
