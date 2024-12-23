from typing import Optional
from video import BURSTVideo

import json
import os.path as osp

import  utils


class BURSTDataset:
    def __init__(self, annotations_file: str, images_base_dir: Optional[str] = None):
        with open(annotations_file, 'r') as fh:
            content = json.load(fh)

        # convert track IDs from str to int wherever they are used as dict keys (JSON format always parses dict keys as
        # strings)
        self._videos = [utils.intify_track_ids(video) for video in content["sequences"]]
        self._videos = list(filter(lambda x: x["dataset"] != "HACS" and x["dataset"] != "AVA" and x["dataset"] != "LaSOT", self._videos))

        self.category_names = {
            category["id"]: category["name"] for category in content["categories"]
        }

        self._split = content["split"]

        self.images_base_dir = images_base_dir

    @property
    def num_videos(self) -> int:
        return len(self._videos)

    def __getitem__(self, index) -> BURSTVideo:
        assert index < self.num_videos, f"Index {index} invalid since total number of videos is {self.num_videos}"

        video_dict = self._videos[index]
        if self.images_base_dir is None:
            video_images_dir = None
        else:
            video_images_dir = osp.join(self.images_base_dir, self._split, video_dict["dataset"], video_dict["seq_name"])
            assert osp.exists(video_images_dir), f"Images directory for video not found at expected path: '{video_images_dir}'"

        return BURSTVideo(video_dict, video_images_dir)

    def __iter__(self):
        for i in range(self.num_videos):
            yield self[i]