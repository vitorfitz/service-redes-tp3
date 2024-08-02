from flask import Blueprint, request, jsonify

from database import game_data

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/api/game/<int:id>", methods=["GET"])
def get_game(id):
    game = list(filter(lambda x: x["id"] == id, game_data))
    if game:
        return jsonify({"game_id": game[0]["id"], "game_stats": game[0]})
    else:
        return jsonify({"error": "Game not found"}), 404


@api_blueprint.route("/api/rank/sunk", methods=["GET"])
def get_games_ranked_sunk():
    count = request.args.get("limit", default=50, type=int)
    index = request.args.get("start", default=0, type=int)-1
    if count > 50:
        return jsonify({"error": "Count should be maximum 50"}), 400
    if index >= len(game_data) or index < 0:
        return jsonify({"error": "Index out of bounds"}), 400

    games_sunk_ranks = sorted(
        game_data, key=lambda x: x.get("sunk_ships", 0), reverse=True
    )
    prev, next = get_neighbor_urls("/api/rank/escaped", index, count)
    return jsonify(
        {
            "ranking": "sunk",
            "limit": count,
            "start": index+1,
            "games": games_sunk_ranks[index: index + count],
            "prev": prev,
            "next": next,
        }
    )


@api_blueprint.route("/api/rank/escaped", methods=["GET"])
def get_games_ranked_escaped():
    count = request.args.get("limit", default=50, type=int)
    index = request.args.get("start", default=0, type=int)-1
    if count > 50:
        return jsonify({"error": "Count should be maximum 50"}), 400
    if index >= len(game_data) or index < 0:
        return jsonify({"error": "Index out of bounds"}), 400

    games_escaped_ranks = sorted(
        game_data, key=lambda x: x.get("escaped_ships", 0))
    prev, next = get_neighbor_urls(
        "/api/rank/escaped", index, count
    )
    return jsonify(
        {
            "ranking": "escaped",
            "limit": count,
            "start": index+1,
            "games": games_escaped_ranks[index: index + count],
            "prev": prev,
            "next": next
        }
    )


def get_neighbor_urls(base, index, count):
    if index < count:
        prev = None
    else:
        prev = base+"?limit="+str(count)+"&start="+str(index-count+1)

    if index+count >= len(game_data):
        next = None
    else:
        next = base + "?limit=" + str(count) + "&start=" + str(index + count+1)

    return prev, next
